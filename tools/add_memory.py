from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.helpers import parse_json_field
from utils import powermem_client


class AddMemoryTool(Tool):
    """Add memory via powermem (sync)."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        messages = tool_parameters.get("messages")
        if messages is None:
            error = "messages is required (str/dict/list)"
            yield self.create_json_message({"status": "ERROR", "message": error, "results": []})
            yield self.create_text_message(error)
            return

        user_id = tool_parameters.get("user_id")
        agent_id = tool_parameters.get("agent_id")
        run_id = tool_parameters.get("run_id")
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
            result = powermem_client.add(self.runtime.credentials, payload)
            results = result.get("results", [])
            # Convert id to string
            for item in results:
                if isinstance(item, dict) and "id" in item:
                    item["id"] = str(item["id"])
            json_msg = {"status": "SUCCESS", "results": results}
            if "relations" in result:
                json_msg["relations"] = result["relations"]
            yield self.create_json_message(json_msg)

            if results:
                lines = ["Add memory completed."]
                for idx, r in enumerate(results, 1):
                    memory_id = r.get('id', '')
                    event = r.get('event', '')
                    memory = r.get('memory', '')
                    lines.append(f"{idx}. ID:{memory_id} [{event}] {memory}")
                yield self.create_text_message("\n".join(lines))
            else:
                yield self.create_text_message("No memory added (empty content or infer returned no action).")
        except Exception as exc:  # noqa: BLE001
            error = f"Failed to add memory: {exc}"
            yield self.create_json_message({"status": "ERROR", "message": error, "results": []})
            yield self.create_text_message(error)

