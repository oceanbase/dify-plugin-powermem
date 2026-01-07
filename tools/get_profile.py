from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils import powermem_client


class GetProfileTool(Tool):
    """Get user profile via powermem UserMemory (sync)."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        # Check if User Profile feature is enabled
        try:
            from powermem import UserMemory
            from utils.powermem_client import get_memory
            
            mem = get_memory(self.runtime.credentials)
            if not isinstance(mem, UserMemory):
                error = "User Profile feature is not enabled. Please enable 'user_profile_enabled' and use OceanBase database in provider settings."
                yield self.create_json_message({"status": "ERROR", "message": error, "profile": {}})
                yield self.create_text_message(error)
                return
        except Exception as e:
            error = f"Failed to check User Profile feature: {str(e)}"
            yield self.create_json_message({"status": "ERROR", "message": error, "profile": {}})
            yield self.create_text_message(error)
            return
        
        user_id = tool_parameters.get("user_id")
        if not user_id:
            error = "user_id is required"
            yield self.create_json_message({"status": "ERROR", "message": error, "profile": {}})
            yield self.create_text_message(error)
            return

        try:
            profile = powermem_client.get_profile(self.runtime.credentials, user_id)
            
            if profile:
                # Convert id to string
                if isinstance(profile, dict) and "id" in profile:
                    profile["id"] = str(profile["id"])
                
                json_msg = {"status": "SUCCESS", "profile": profile}
                yield self.create_json_message(json_msg)
                
                # Build text message
                lines = [f"User Profile for user_id: {user_id}"]
                if profile.get("profile_content"):
                    lines.append(f"Content: {profile['profile_content']}")
                if profile.get("topics"):
                    lines.append("Topics:")
                    topics = profile["topics"]
                    for key, value in topics.items():
                        lines.append(f"  - {key}: {value}")
                if profile.get("created_at"):
                    lines.append(f"Created: {profile['created_at']}")
                if profile.get("updated_at"):
                    lines.append(f"Updated: {profile['updated_at']}")
                yield self.create_text_message("\n".join(lines))
            else:
                msg = f"No profile found for user_id: {user_id}"
                yield self.create_json_message({"status": "SUCCESS", "profile": {}})
                yield self.create_text_message(msg)
        except Exception as exc:  # noqa: BLE001
            error = f"Failed to get profile: {exc}"
            yield self.create_json_message({"status": "ERROR", "message": error, "profile": {}})
            yield self.create_text_message(error)


