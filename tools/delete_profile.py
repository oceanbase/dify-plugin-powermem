from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils import powermem_client


class DeleteProfileTool(Tool):
    """Delete user profile via powermem UserMemory (sync)."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        # Check if User Profile feature is enabled
        try:
            from powermem import UserMemory
            from utils.powermem_client import get_memory
            
            mem = get_memory(self.runtime.credentials)
            if not isinstance(mem, UserMemory):
                error = "User Profile feature is not enabled. Please enable 'user_profile_enabled' and use OceanBase database in provider settings."
                yield self.create_json_message({"status": "ERROR", "message": error, "success": False})
                yield self.create_text_message(error)
                return
        except Exception as e:
            error = f"Failed to check User Profile feature: {str(e)}"
            yield self.create_json_message({"status": "ERROR", "message": error, "success": False})
            yield self.create_text_message(error)
            return
        
        user_id = tool_parameters.get("user_id")
        if not user_id:
            error = "user_id is required"
            yield self.create_json_message({"status": "ERROR", "message": error, "success": False})
            yield self.create_text_message(error)
            return

        try:
            success = powermem_client.delete_profile(self.runtime.credentials, user_id)
            
            if success:
                yield self.create_json_message({"status": "SUCCESS", "success": True})
                yield self.create_text_message(f"Profile deleted for user_id: {user_id}")
            else:
                msg = f"Profile not found for user_id: {user_id}"
                yield self.create_json_message({"status": "SUCCESS", "success": False, "message": msg})
                yield self.create_text_message(msg)
        except Exception as exc:  # noqa: BLE001
            error = f"Failed to delete profile: {exc}"
            yield self.create_json_message({"status": "ERROR", "message": error, "success": False})
            yield self.create_text_message(error)


