## PowerMem [![PowerMem](https://img.shields.io/badge/PowerMem-blue)](https://www.powermem.ai/)

**Author:** oceanbase  
**Version:** 0.0.3  
**Type:** tool  

### Description
- Dify plugin wrapping PowerMem SDK (sync tools) for workflows and agent strategies.
- Tools: add_memory / search_memories / update_memory / delete_all_memories / list_memories / get_profile / list_profiles / delete_profile.
- Outputs JSON (status/results/relations etc. directly from SDK) + text; timestamps are ISO strings.

### Tools Introduction
1. **add_memory**: add or intelligently merge; messages (str/JSON list/dict), user_id/agent_id/run_id, metadata (JSON string), infer (default true). When User Profile is enabled, user_id is required; text output will show user_id and profile summary.  
2. **search_memories**: vector/hybrid search; query, user_id/agent_id/run_id, limit, threshold, filters (JSON string), add_profile (bool; requires user_id to return profile).  
3. **update_memory**: update by memory_id with content/metadata.  
4. **delete_all_memories**: delete all by user_id/agent_id/run_id scope.  
5. **list_memories**: list memories; filters (JSON string), limit/offset, user_id/agent_id/run_id.  
6. **get_profile**: get user profile by user_id (requires User Profile enabled and OceanBase).  
7. **list_profiles**: list user profiles with topic filters (requires User Profile enabled and OceanBase).  
8. **delete_profile**: delete user profile by user_id (requires User Profile enabled and OceanBase).  

### Usage Instructions
1. Credentials: llm_provider (qwen/openai/siliconflow/deepseek; default qwen), llm_api_key, llm_model (default qwen-plus); embedder_provider (qwen/openai; default qwen), embedder_api_key, embedder_model (default text-embedding-v4), embedder_dims (default 1536); db_provider (default sqlite).  
2. If using oceanbase, fill host/port/user/password/database, optionally graph_store_enabled (graph, OceanBase only) and user_profile_enabled (User Profile, OceanBase only).

### Agent System Prompt Template
Copy and use the following as the Agent **system prompt** (edit as needed):

```text
You are a conversational assistant. Use tools flexibly to manage memories and build a user profile.
User Profile feature is enabled (user_profile_enabled=true) and the database is OceanBase (db_provider=oceanbase).
{{user_id}} is the user's user_id.
Prefer using the add_memory tool to record/store memories.

Tool usage rules:
- add_memory: Record/store long-term memories. Prefer passing `messages` as plain text (the SDK will normalize it). Only use OpenAI-style JSON (`{"role","content"}` or a list of them) when you need multi-turn context or explicit roles. Prefer `infer=true` by default; only use `infer=false` when the user explicitly asks for deterministic "store as-is / no intelligent merge". When User Profile is enabled, you must pass `user_id`.
- search_memories: Retrieve relevant memories. Pass `user_id` by default to keep user isolation. To include user profile in the result, set `add_profile=true` AND you must pass `user_id`; the result may include top-level `profile_content` / `topics` (if available). Optional: `limit` / `threshold` / `filters` (`filters` is a JSON string object).
- list_memories: List memories by scope (useful for debugging). Optional `user_id`/`agent_id`/`run_id` + `limit`/`offset`; `filters` is a JSON string object (also affects graph-side results when Graph Store is enabled).
- update_memory: Update memory content when `memory_id` is known (optionally pass `user_id`/`agent_id` as scope). `metadata` is a JSON string object; if omitted, the SDK will try to reuse existing metadata.
- get_profile: Get the user profile for `user_id` (returns a dict or an empty dict). Only available when User Profile is enabled (user_profile_enabled=true AND db_provider=oceanbase).
- list_profiles: List user profiles (pagination via `limit`/`offset`). `main_topic`/`sub_topic`/`topic_value` are JSON string arrays; `sub_topic` path format is "main_topic.sub_topic". Only available when User Profile is enabled (user_profile_enabled=true AND db_provider=oceanbase).
- delete_profile: Delete the user profile for `user_id` (dangerous). Only available when User Profile is enabled (user_profile_enabled=true AND db_provider=oceanbase). You MUST ask for an explicit second confirmation; only call after the user clearly confirms.
- delete_all_memories: Delete memories by scope (dangerous; empty scope may delete everything). You MUST ask for an explicit second confirmation; only call after the user clearly confirms.
```

### Notes
- infer=true uses intelligent mode; infer=false uses simple mode.  
- OceanBase only when DB Type is oceanbase; default sqlite.  
- Ensure the OceanBase database exists before using it as vector store.  
- seekdb as light OceanBase: choose DB Type to be oceanbase and fill seekdb connection to use it as vector store.  
- Scope user_id/agent_id etc. affects search/update/delete; leave empty for no scope.  
- User Profile feature is only available when `user_profile_enabled=true` and `db_provider=oceanbase`; otherwise profile tools will return a friendly error and search `add_profile` will not return profile.  
- Graph feature (`graph_store_enabled`) is only available when `db_provider=oceanbase` and uses the same OceanBase connection parameters.  

### Version History
| Version | Date    | Changes        |
|---------|---------|----------------|
| v0.0.3  | 2026-01-07 | PowerMem 0.2.1 SDK, keep raw JSON return, improve text output and add user profile tools |
| v0.0.2  | 2025-12-17 | Enhanced workflow text output with ID and key fields, use PowerMem 0.2.0 SDK |
| v0.0.1  | Initial | First release  |

### Contributing
- [PowerMem](https://github.com/oceanbase/powermem) main repo  
- [dify-plugin-powermem](https://github.com/oceanbase/dify-plugin-powermem) plugin repo