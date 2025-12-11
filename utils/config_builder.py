from __future__ import annotations

import json
from typing import Any, Dict


def _default_config() -> Dict[str, Any]:
    """Default config: sqlite only (single-mode) with basic llm/embedder defaults."""
    db_provider = "sqlite"
    sqlite_config = {
        "database_path": "./data/powermem_dev.db",
        "collection_name": "memories",
        "enable_wal": True,
        "timeout": 30,
    }

    llm_provider = "qwen"
    llm_config = {
        "api_key": None,
        "model": "qwen-plus",
        "temperature": 0.7,
        "max_tokens": 1000,
        "top_p": 0.8,
        "top_k": 50,
        "enable_search": False,
    }

    embedder_config = {
        "api_key": None,
        "model": "text-embedding-v4",
        "embedding_dims": 1536,
    }

    config = {
        "vector_store": {"provider": db_provider, "config": sqlite_config},
        "llm": {"provider": llm_provider, "config": llm_config},
        "embedder": {"provider": "qwen", "config": embedder_config},
        "intelligent_memory": {
            "enabled": True,
            "initial_retention": 1.0,
            "decay_rate": 0.1,
            "reinforcement_factor": 0.3,
            "working_threshold": 0.3,
            "short_term_threshold": 0.6,
            "long_term_threshold": 0.8,
        },
        "agent_memory": {
            "enabled": True,
            "mode": "auto",
            "default_scope": "AGENT",
            "default_privacy_level": "PRIVATE",
            "default_collaboration_level": "READ_ONLY",
            "default_access_permission": "OWNER_ONLY",
        },
        "telemetry": {
            "enable_telemetry": False,
            "telemetry_endpoint": "https://telemetry.powermem.ai",
            "telemetry_api_key": None,
            "telemetry_batch_size": 100,
            "telemetry_flush_interval": 30,
        },
        "audit": {
            "enabled": True,
            "log_file": "./logs/audit.log",
            "log_level": "INFO",
            "retention_days": 90,
        },
        "logging": {
            "level": "DEBUG",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": "./logs/powermem.log",
        },
        "reranker": {
            "enabled": False,
            "provider": "qwen",
            "config": {"model": None, "api_key": None},
        },
    }
    return config


def build_config(credentials: dict[str, Any]) -> dict[str, Any]:
    """
    Build powermem config with minimal inputs:
    - start with sqlite defaults
    - override llm/embedder provider/model/api_key if provided as separate fields
    - switch vector_store when db_provider=oceanbase (uses provided OB connection info)
    """
    config = _default_config()

    db_provider = (credentials.get("db_provider") or "sqlite").lower()
    if db_provider == "oceanbase":
        ob_host = credentials.get("oceanbase_host") or "127.0.0.1"
        ob_port = credentials.get("oceanbase_port") or 2881
        ob_user = credentials.get("oceanbase_user") or "root@sys"
        ob_password = credentials.get("oceanbase_password", "")
        ob_db_name = credentials.get("oceanbase_database") or "powermem"

        oceanbase_config = {
            "collection_name": "memories",
            "connection_args": {
                "host": ob_host,
                "port": ob_port,
                "user": ob_user,
                "password": ob_password,
                "db_name": ob_db_name,
            },
            "vidx_metric_type": "cosine",
            "index_type": "IVF_FLAT",
            "embedding_model_dims": 1536,
            "primary_field": "id",
            "vector_field": "embedding",
            "text_field": "document",
            "metadata_field": "metadata",
            "vidx_name": "memories_vidx",
        }

        config["vector_store"] = {"provider": "oceanbase", "config": oceanbase_config}

    # LLM provider/model/config
    llm_provider = (credentials.get("llm_provider") or "qwen").lower()
    config["llm"]["provider"] = llm_provider
    llm_conf = config["llm"].setdefault("config", {})
    llm_conf["api_key"] = credentials.get("llm_api_key")
    llm_conf["model"] = credentials.get("llm_model") or "qwen-plus"
    if llm_provider == "qwen":
        llm_conf["dashscope_base_url"] = "https://dashscope.aliyuncs.com/api/v1"
    elif llm_provider == "openai":
        llm_conf["openai_base_url"] = "https://api.openai.com/v1"

    # Embedder provider/model/config
    embedder_provider = (credentials.get("embedder_provider") or "qwen").lower()
    config["embedder"]["provider"] = embedder_provider
    emb_conf = config["embedder"].setdefault("config", {})
    emb_conf["api_key"] = credentials.get("embedder_api_key")
    emb_conf["model"] = credentials.get("embedder_model") or "text-embedding-v4"

    return config

