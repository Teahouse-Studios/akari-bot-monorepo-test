"""服务器清理和重启模块。"""

import asyncio
import os

from tortoise import Tortoise

# from core.builtins.session.tasks import SessionTaskManager
from akaribot.core.logger import Logger
from akaribot.core.module_runtime import ModuleRuntimeManager
from akaribot.core.queue.server import JobQueueServer
from akaribot.core.scheduler import SchedulerLifecycle
from akaribot.core.utils.web_render import close_web_render
from .background_tasks import stop_background_task
from .lifecycle import BackgroundTaskLifecycle


async def cleanup_sessions():
    """清理服务器资源。"""
    # get_wait_list = SessionTaskManager.get()
    Logger.warning("Cleaning up sessions...")
    SchedulerLifecycle.begin_shutdown()
    # 先关闭新操作入口并与已经开始认领的一轮轮询建立屏障。轮询器仍继续回收
    # 执行中 RPC 的远端结果，供后续取消任务时释放平台上下文。
    await JobQueueServer.begin_shutdown()
    # 队列处理器可能持有 Scheduler 维护锁，也可能在退出路径创建独立任务。
    # 先取消并等待它们，再关闭 Scheduler，最后统一清理所有已注册后台任务。
    await JobQueueServer.cancel_process_tasks()
    try:
        await SchedulerLifecycle.shutdown()
    except Exception:
        Logger.exception("Failed to stop scheduler cleanly.")
    try:
        await stop_background_task()
    except Exception:
        Logger.exception("Failed to stop background initialization cleanly.")
    await ModuleRuntimeManager.shutdown()
    # 注册项可能持有 MessageSession 上下文，需要在停止轮询器之前取消。
    # 仅实际导入过的组件会执行注册，关闭阶段不为清理额外导入模块。
    await BackgroundTaskLifecycle.run_cleanup()
    # restart() 可能通过队列操作自身触发，此时主循环的轮询器仍在运行。关闭窗口
    # 必须先阻止它继续认领任务，再取消其他处理器，并在独占轮询锁时关闭资源。
    # 不可清空全局队列表，因为同一 service 的其他 Server 实例仍可能依赖其中的任务。
    async with JobQueueServer.shutdown_window():
        # 独立任务的上下文已经释放，后续不需要继续轮询远端结果。先停止轮询器，
        # 再在持有 _poll_lock 时关闭依赖，避免窗口退出后轮询已关闭的数据库。
        await JobQueueServer.stop_job_queue()
        try:
            await asyncio.wait_for(close_web_render(), timeout=10)
        except TimeoutError:
            Logger.warning("Timed out while closing WebRender.")
        except Exception:
            Logger.exception("Failed to close WebRender cleanly.")
        try:
            await Tortoise.close_connections()
        except Exception:
            Logger.exception("Failed to close database connections cleanly.")


async def restart():
    """重启服务器。"""
    await cleanup_sessions()
    os._exit(33)
