from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.helpers import parse_json_field
from utils import powermem_client


class ListProfilesTool(Tool):
    """List user profiles via powermem UserMemory (sync)."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        # Check if User Profile feature is enabled
        try:
            from powermem import UserMemory
            from utils.powermem_client import get_memory
            
            mem = get_memory(self.runtime.credentials)
            if not isinstance(mem, UserMemory):
                error = "User Profile feature is not enabled. Please enable 'user_profile_enabled' and use OceanBase database in provider settings."
                yield self.create_json_message({"status": "ERROR", "message": error, "profiles": []})
                yield self.create_text_message(error)
                return
        except Exception as e:
            error = f"Failed to check User Profile feature: {str(e)}"
            yield self.create_json_message({"status": "ERROR", "message": error, "profiles": []})
            yield self.create_text_message(error)
            return
        
        params: dict[str, Any] = {}
        
        # Handle user_id
        user_id = tool_parameters.get("user_id")
        if user_id:
            params["user_id"] = user_id
        
        # Handle main_topic (JSON array)
        main_topic_raw = tool_parameters.get("main_topic")
        if main_topic_raw:
            main_topic, err = parse_json_field(main_topic_raw, "main_topic")
            if err:
                yield self.create_json_message({"status": "ERROR", "message": err, "profiles": []})
                yield self.create_text_message(err)
                return
            if main_topic and isinstance(main_topic, list):
                params["main_topic"] = main_topic
        
        # Handle sub_topic (JSON array)
        sub_topic_raw = tool_parameters.get("sub_topic")
        if sub_topic_raw:
            sub_topic, err = parse_json_field(sub_topic_raw, "sub_topic")
            if err:
                yield self.create_json_message({"status": "ERROR", "message": err, "profiles": []})
                yield self.create_text_message(err)
                return
            if sub_topic and isinstance(sub_topic, list):
                params["sub_topic"] = sub_topic
        
        # Handle topic_value (JSON array)
        topic_value_raw = tool_parameters.get("topic_value")
        if topic_value_raw:
            topic_value, err = parse_json_field(topic_value_raw, "topic_value")
            if err:
                yield self.create_json_message({"status": "ERROR", "message": err, "profiles": []})
                yield self.create_text_message(err)
                return
            if topic_value and isinstance(topic_value, list):
                params["topic_value"] = topic_value
        
        # Handle limit and offset
        params["limit"] = tool_parameters.get("limit", 100)
        params["offset"] = tool_parameters.get("offset", 0)

        try:
            profiles = powermem_client.list_profiles(self.runtime.credentials, params)
            
            # Convert id to string
            for profile in profiles:
                if isinstance(profile, dict) and "id" in profile:
                    profile["id"] = str(profile["id"])
            
            json_msg = {"status": "SUCCESS", "profiles": profiles}
            yield self.create_json_message(json_msg)
            
            # Build text message
            lines = [f"Found {len(profiles)} profile(s)"]
            for idx, profile in enumerate(profiles, 1):
                lines.append(f"\n{idx}. User ID: {profile.get('user_id', 'N/A')}")
                if profile.get("profile_content"):
                    lines.append(f"   Content: {profile['profile_content']}")
                if profile.get("topics"):
                    lines.append("   Topics:")
                    topics = profile["topics"]
                    for key, value in topics.items():
                        lines.append(f"     - {key}: {value}")
                if profile.get("updated_at"):
                    lines.append(f"   Updated: {profile['updated_at']}")
            
            yield self.create_text_message("\n".join(lines))
        except Exception as exc:  # noqa: BLE001
            error = f"Failed to list profiles: {exc}"
            yield self.create_json_message({"status": "ERROR", "message": error, "profiles": []})
            yield self.create_text_message(error)


