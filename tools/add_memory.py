from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.helpers import parse_json_field
from utils import powermem_client
from utils.powermem_client import get_memory


class AddMemoryTool(Tool):
    """Add memory via powermem (sync)."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        messages = tool_parameters.get("messages")
        if messages is None:
            error = "messages is required (str/dict/list)"
            yield self.create_json_message({"status": "ERROR", "message": error, "results": []})
            yield self.create_text_message(error)
            return

        user_id = tool_parameters.get("user_id") or None
        agent_id = tool_parameters.get("agent_id") or None
        run_id = tool_parameters.get("run_id") or None
        metadata_raw = tool_parameters.get("metadata")
        metadata, meta_err = parse_json_field(metadata_raw, "metadata")
        if meta_err:
            yield self.create_json_message({"status": "ERROR", "message": meta_err, "results": []})
            yield self.create_text_message(meta_err)
            return
        infer = tool_parameters.get("infer")
        if infer is None:
            infer = True

        payload: dict[str, Any] = {
            "messages": messages,
            "user_id": user_id,
            "agent_id": agent_id,
            "run_id": run_id,
            "metadata": metadata,
            "infer": bool(infer),
        }

        try:
            # Check if UserMemory is being used and user_id is required
            mem = get_memory(self.runtime.credentials)
            from powermem import UserMemory
            if isinstance(mem, UserMemory) and not user_id:
                error = "user_id is required when User Profile feature is enabled"
                yield self.create_json_message({"status": "ERROR", "message": error, "results": []})
                yield self.create_text_message(error)
                return
            
            result = powermem_client.add(self.runtime.credentials, payload)
            results = result.get("results", [])
            # Convert id to string
            for item in results:
                if isinstance(item, dict) and "id" in item:
                    item["id"] = str(item["id"])
            
            json_msg = {"status": "SUCCESS"}
            json_msg.update(result)
            yield self.create_json_message(json_msg)

            # Build text message
            if results:
                lines = ["Add memory completed."]
                for idx, r in enumerate(results, 1):
                    memory_id = str(r.get('id', ''))
                    event = r.get('event', '')
                    memory = r.get('memory', '')
                    lines.append(f"{idx}. ID:{memory_id} [{event}] {memory}")
                
                # Add user profile information if present (UserMemory feature)
                if result.get("profile_extracted"):
                    lines.append("")
                    # Use the input user_id parameter
                    if user_id:
                        lines.append(f"User Profile Extracted (user_id: {user_id}):")
                    else:
                        lines.append("User Profile Extracted:")
                    if result.get("profile_content"):
                        lines.append(f"  Content: {result['profile_content']}")
                    if result.get("topics"):
                        lines.append("  Topics:")
                        topics = result["topics"]
                        for key, value in topics.items():
                            lines.append(f"    - {key}: {value}")
                
                yield self.create_text_message("\n".join(lines))
            else:
                yield self.create_text_message("No memory added (empty content or infer returned no action).")
        except Exception as exc:  # noqa: BLE001
            error = f"Failed to add memory: {exc}"
            yield self.create_json_message({"status": "ERROR", "message": error, "results": []})
            yield self.create_text_message(error)

