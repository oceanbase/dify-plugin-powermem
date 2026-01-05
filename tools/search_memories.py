from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.helpers import parse_json_field
from utils import powermem_client


class SearchMemoriesTool(Tool):
    """Search memories via powermem (sync)."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        query = tool_parameters.get("query")
        if not query:
            error = "query is required"
            yield self.create_json_message({"status": "ERROR", "message": error, "results": []})
            yield self.create_text_message(error)
            return

        user_id = tool_parameters.get("user_id") or None
        agent_id = tool_parameters.get("agent_id") or None
        run_id = tool_parameters.get("run_id") or None
        limit = tool_parameters.get("limit", 30)
        threshold = tool_parameters.get("threshold")
        add_profile = tool_parameters.get("add_profile", False)

        filters_raw = tool_parameters.get("filters")
        filters, filters_err = parse_json_field(filters_raw, "filters")
        if filters_err:
            yield self.create_json_message({"status": "ERROR", "message": filters_err, "results": []})
            yield self.create_text_message(filters_err)
            return

        payload: dict[str, Any] = {
            "query": query,
            "user_id": user_id,
            "agent_id": agent_id,
            "run_id": run_id,
            "limit": limit,
            "threshold": threshold,
            "filters": filters,
            "add_profile": add_profile,
        }

        try:
            result = powermem_client.search(self.runtime.credentials, payload)
            results = result.get("results", [])
            # Convert id to string
            for item in results:
                if isinstance(item, dict) and "id" in item:
                    item["id"] = str(item["id"])
            
            json_msg = {"status": "SUCCESS"}
            json_msg.update(result)
            yield self.create_json_message(json_msg)

            # text summary
            lines = [f"Query: {query}", f"Found: {len(results)}"]
            for idx, r in enumerate(results, 1):
                memory_id = str(r.get('id', ''))
                memory = r.get('memory', '')
                user_id = r.get('user_id', '')
                agent_id = r.get('agent_id', '')
                run_id = r.get('run_id', '')
                score = r.get('score')
                
                lines.append(f"{idx}. ID:{memory_id} {memory}")
                if score is not None:
                    lines.append(f"   score: {score}")
                if user_id:
                    lines.append(f"   user_id: {user_id}")
                if agent_id:
                    lines.append(f"   agent_id: {agent_id}")
                if run_id:
                    lines.append(f"   run_id: {run_id}")
            
            # Add user profile information if present (UserMemory feature)
            if result.get("profile_content") or result.get("topics"):
                lines.append("")
                lines.append("User Profile:")
                if result.get("profile_content"):
                    lines.append(f"  Content: {result['profile_content']}")
                if result.get("topics"):
                    lines.append("  Topics:")
                    topics = result["topics"]
                    for key, value in topics.items():
                        lines.append(f"    - {key}: {value}")
            
            yield self.create_text_message("\n".join(lines))
        except Exception as exc:  # noqa: BLE001
            error = f"Failed to search memories: {exc}"
            yield self.create_json_message({"status": "ERROR", "message": error, "results": []})
            yield self.create_text_message(error)

