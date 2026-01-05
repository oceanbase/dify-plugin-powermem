from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.helpers import parse_json_field
from utils import powermem_client


class UpdateMemoryTool(Tool):
    """Update memory via powermem (sync)."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        memory_id = tool_parameters.get("memory_id")
        content = tool_parameters.get("content")
        if memory_id is None or not content:
            error = "memory_id and content are required"
            yield self.create_json_message({"status": "ERROR", "message": error, "results": {}})
            yield self.create_text_message(error)
            return

        user_id = tool_parameters.get("user_id") or None
        agent_id = tool_parameters.get("agent_id") or None
        metadata_raw = tool_parameters.get("metadata")
        metadata, meta_err = parse_json_field(metadata_raw, "metadata")
        if meta_err:
            yield self.create_json_message({"status": "ERROR", "message": meta_err, "results": {}})
            yield self.create_text_message(meta_err)
            return

        try:
            result = powermem_client.update(
                self.runtime.credentials,
                int(memory_id),
                content,
                user_id,
                agent_id,
                metadata,
            )
            if not result:
                msg = f"Memory {memory_id} not found"
                yield self.create_json_message({"status": "ERROR", "message": msg, "results": {}})
                yield self.create_text_message(msg)
                return
            # Convert id to string
            if isinstance(result, dict) and "id" in result:
                result["id"] = str(result["id"])
            
            json_msg = {"status": "SUCCESS"}
            json_msg.update(result)
            yield self.create_json_message(json_msg)
            
            updated_id = str(result.get('id', memory_id))
            yield self.create_text_message(f"Memory updated. ID:{updated_id}")
        except Exception as exc:  # noqa: BLE001
            error = f"Failed to update memory: {exc}"
            yield self.create_json_message({"status": "ERROR", "message": error, "results": {}})
            yield self.create_text_message(error)

