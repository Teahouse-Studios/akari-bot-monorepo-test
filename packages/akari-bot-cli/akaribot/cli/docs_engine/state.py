"""文档构建与部署状态的持久化。

状态写在实例根的 ``.docs/state.json``，只记录构建指纹与部署历史；缓存复用与实际部署都以它为准，
写入一律原子替换，避免中断留下半截 JSON。
"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

STATE_VERSION = 1
STATE_DIR = ".docs"
STATE_FILENAME = "state.json"
DEPLOY_HISTORY_LIMIT = 50


def state_path(instance: Any) -> Path:
    """状态文件路径。"""
    return Path(instance.root) / STATE_DIR / STATE_FILENAME


def load_state(instance: Any) -> dict[str, Any]:
    """读取状态；文件缺失或损坏时返回空状态，构建据此重新生成。"""
    path = state_path(instance)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeDecodeError):
        return _empty_state()
    if not isinstance(payload, Mapping) or payload.get("schema") != STATE_VERSION:
        return _empty_state()
    state = _empty_state()
    state.update(payload)
    state["schema"] = STATE_VERSION
    if not isinstance(state.get("build"), Mapping):
        state["build"] = None
    if not isinstance(state.get("deploys"), list):
        state["deploys"] = []
    return state


def save_build_state(
    instance: Any,
    *,
    fingerprint: str,
    packages: Sequence[str],
    out_dir: Path,
    base: str,
    at: str | None = None,
) -> Path:
    """记录最近一次成功构建。"""
    state = load_state(instance)
    state["build"] = {
        "fingerprint": fingerprint,
        "packages": list(packages),
        "out_dir": str(out_dir),
        "base": base,
        "generated_at": at or _now(),
    }
    return _write_state(instance, state)


def record_deploy(
    instance: Any,
    target: str,
    *,
    status: str = "ok",
    detail: str = "",
    at: str | None = None,
) -> Path:
    """追加一条部署记录，超出上限时丢弃最旧的条目。

    :param instance: 实例。
    :param target: 部署目标，如远端路径或分支名。
    :param status: 结果标签。
    :param detail: 补充说明。
    :return: 状态文件路径。
    """
    state = load_state(instance)
    deploys = list(state.get("deploys") or [])
    deploys.append({"target": target, "status": status, "detail": detail, "at": at or _now()})
    state["deploys"] = deploys[-DEPLOY_HISTORY_LIMIT:]
    return _write_state(instance, state)


def _write_state(instance: Any, state: dict[str, Any]) -> Path:
    path = state_path(instance)
    path.parent.mkdir(parents=True, exist_ok=True)
    state["schema"] = STATE_VERSION
    temporary = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)
    return path


def _empty_state() -> dict[str, Any]:
    return {"schema": STATE_VERSION, "build": None, "deploys": []}


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
