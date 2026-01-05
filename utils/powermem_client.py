from __future__ import annotations

import threading
from datetime import date, datetime
from hashlib import sha256
from typing import Any, Dict, Optional

from powermem import create_memory
from utils.config_builder import build_config

_memory = None
_memory_hash: Optional[str] = None
_lock = threading.Lock()


def _hash_config(config: dict[str, Any]) -> str:
    try:
        import json

        return sha256(json.dumps(config, sort_keys=True, default=str).encode()).hexdigest()
    except Exception:
        return ""


def _convert_dt(obj: Any) -> Any:
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _convert_dt(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_convert_dt(v) for v in obj]
    return obj


def get_memory(credentials: dict[str, Any]):
    global _memory, _memory_hash  # noqa: PLW0603
    config = build_config(credentials)
    config_hash = _hash_config(config)
    with _lock:
        if _memory is None or _memory_hash != config_hash:
            # Check if user profile feature is enabled
            user_profile_enabled = credentials.get("user_profile_enabled") is True
            db_provider = credentials.get("db_provider", "sqlite").lower()
            
            # User profile feature is only available with OceanBase
            if user_profile_enabled and db_provider == "oceanbase":
                from powermem import UserMemory
                _memory = UserMemory(config=config)
            else:
                _memory = create_memory(config=config)
            
            _memory_hash = config_hash
    return _memory


def add(credentials: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    mem = get_memory(credentials)
    return _convert_dt(mem.add(**payload))


def search(credentials: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    mem = get_memory(credentials)
    return _convert_dt(mem.search(**payload))


def update(credentials: dict[str, Any], memory_id: int, content: str, user_id: str | None, agent_id: str | None, metadata: dict | None) -> dict[str, Any] | None:
    mem = get_memory(credentials)
    return _convert_dt(mem.update(memory_id=memory_id, content=content, user_id=user_id, agent_id=agent_id, metadata=metadata))


def delete_all(credentials: dict[str, Any], user_id: str | None, agent_id: str | None, run_id: str | None) -> bool:
    mem = get_memory(credentials)
    return bool(mem.delete_all(user_id=user_id, agent_id=agent_id, run_id=run_id))


def get_all(credentials: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    mem = get_memory(credentials)
    return _convert_dt(mem.get_all(**params))


def get_profile(credentials: dict[str, Any], user_id: str) -> dict[str, Any]:
    mem = get_memory(credentials)
    return _convert_dt(mem.profile(user_id=user_id))


def list_profiles(credentials: dict[str, Any], params: dict[str, Any]) -> list[dict[str, Any]]:
    mem = get_memory(credentials)
    return _convert_dt(mem.profile_list(**params))


def delete_profile(credentials: dict[str, Any], user_id: str) -> bool:
    mem = get_memory(credentials)
    return bool(mem.delete_profile(user_id=user_id))

