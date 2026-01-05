from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils import powermem_client


class DeleteAllMemoriesTool(Tool):
    """Delete all memories via powermem (sync)."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        user_id = tool_parameters.get("user_id") or None
        agent_id = tool_parameters.get("agent_id") or None
        run_id = tool_parameters.get("run_id") or None

        try:
            success = powermem_client.delete_all(self.runtime.credentials, user_id, agent_id, run_id)
            if success:
                yield self.create_json_message({"status": "SUCCESS", "success": True})
                yield self.create_text_message("All memories deleted.")
            else:
                msg = "Delete all failed"
                yield self.create_json_message({"status": "ERROR", "success": False, "message": msg})
                yield self.create_text_message(msg)
        except Exception as exc:  # noqa: BLE001
            error = f"Failed to delete all memories: {exc}"
            yield self.create_json_message({"status": "ERROR", "message": error})
            yield self.create_text_message(error)

