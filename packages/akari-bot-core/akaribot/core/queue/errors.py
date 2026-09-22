"""Stable RPC failures shared by both sides of the process boundary."""


class RpcError(Exception):
    code = "rpc_error"

    def __init__(
        self,
        message: str,
        *,
        method: str = "",
        target: str = "",
        task_id: str = "",
        remote_type: str = "",
        traceback: str = "",
        caller_traceback: str = "",
        remote_traceback: str | None = None,
    ):
        super().__init__(message)
        self.method = method
        self.target = target
        self.task_id = task_id
        self.remote_type = remote_type
        # 异常对象以 JSON 跨 RPC，故合并诊断文本与原始进程栈分别保留。
        # ``remote_traceback`` 为可选：旧响应信封只带一个 traceback 字段。
        self.traceback = traceback
        self.remote_traceback = traceback if remote_traceback is None else remote_traceback
        self.caller_traceback = caller_traceback


class RpcTimeoutError(RpcError, TimeoutError):
    """The deadline expired; a remote side effect may already have happened."""

    code = "timeout"


class RpcRemoteError(RpcError):
    code = "remote_error"


class RpcMethodNotFoundError(RpcRemoteError):
    code = "method_not_found"


class RpcUnavailableError(RpcError):
    code = "unavailable"


class RpcCancelledError(RpcRemoteError):
    """The receiving process stopped an in-flight handler without retrying it."""

    code = "cancelled"


class RpcProtocolError(RpcError):
    code = "protocol_error"


ERROR_TYPES = {
    error.code: error
    for error in (
        RpcTimeoutError,
        RpcRemoteError,
        RpcMethodNotFoundError,
        RpcUnavailableError,
        RpcCancelledError,
        RpcProtocolError,
    )
}
