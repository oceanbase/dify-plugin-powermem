## PowerMem [![PowerMem](https://img.shields.io/badge/PowerMem-blue)](https://www.powermem.ai/)

**Author:** oceanbase  
**Version:** 0.0.2  
**Type:** tool  

### Description
- Dify plugin wrapping PowerMem SDK (sync tools) for workflows and agent strategies.
- Tools: add_memory / search_memories / update_memory / delete_all_memories / list_memories.
- Outputs JSON (status/results/relations) + text; timestamps are ISO strings.

### Tools Introduction
1. **add_memory**: add or intelligently merge; messages (str/JSON list/dict), user_id/agent_id/run_id, metadata (JSON string), infer (default true).  
2. **search_memories**: vector/hybrid search; query, user_id/agent_id/run_id, limit, threshold, filters (JSON string).  
3. **update_memory**: update by memory_id with content/metadata.  
4. **delete_all_memories**: delete all by user_id/agent_id/run_id scope.  
5. **list_memories**: list memories; filters (JSON string), limit/offset, user_id/agent_id/run_id.  

### Usage Instructions
1. Credentials: llm_provider (default qwen), llm_api_key, llm_model (default qwen-plus); embedder_provider (default qwen), embedder_api_key, embedder_model (default text-embedding-v4); db_provider (default sqlite).  
2. If using oceanbase, fill host/port/user/password/database.

### Notes
- infer=true uses intelligent mode; infer=false uses simple mode.  
- OceanBase only when DB Type is oceanbase; default sqlite.  
- Ensure the OceanBase database exists before using it as vector store.  
- seekdb as light OceanBase: choose DB Type to be oceanbase and fill seekdb connection to use it as vector store.  
- Scope user_id/agent_id affects search/update/delete; leave empty for no scope.  

### Version History
| Version | Date    | Changes        |
|---------|---------|----------------|
| v0.0.2  | 2024-12 | Enhanced workflow text output with ID and key fields, use PowerMem 0.2.0 SDK |
| v0.0.1  | Initial | First release  |

### Contributing
- [PowerMem](https://github.com/oceanbase/powermem) main repo  
- [dify-plugin-powermem](https://github.com/oceanbase/dify-plugin-powermem) plugin repo