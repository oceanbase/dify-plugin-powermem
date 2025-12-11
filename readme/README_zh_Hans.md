## PowerMem [![PowerMem](https://img.shields.io/badge/PowerMem-blue)](https://www.powermem.ai/)

**Author:** oceanbase  
**Version:** 0.0.1  
**Type:** tool  

### 简介
- 封装 PowerMem SDK 的同步工具，适用于 Dify 工作流和 Agent 策略。
- 提供 5 个工具：add_memory / search_memories / update_memory / delete_all_memories / list_memories。
- 返回 JSON（status/results/relations）+ text；时间为 ISO 字符串。

### 工具说明
1. **add_memory**：新增或智能合并记忆；messages（字符串或 JSON 列表/字典）、user_id/agent_id/run_id、metadata(JSON 字符串)、infer（默认 true）。  
2. **search_memories**：向量/混合检索记忆；query、user_id/agent_id/run_id、limit、threshold、filters(JSON 字符串)。  
3. **update_memory**：按 memory_id（字符串传入、内部转 int）更新 content，可带 metadata。  
4. **delete_all_memories**：按 user_id/agent_id/run_id 范围删除全部。  
5. **list_memories**：列出记忆；filters(JSON 字符串)、limit/offset、user_id/agent_id/run_id。  

### 使用说明
1. 配置凭证：llm_provider（默认 qwen）、llm_api_key、llm_model（默认 qwen-plus）；embedder_provider（默认 qwen）、embedder_api_key、embedder_model（默认 text-embedding-v4）；db_provider（默认 sqlite）。  
2. 如选 oceanbase，填写 host/port/user/password/database。

### 版本历史
| 版本    | 日期    | 变更           |
|---------|--------|----------------|
| v0.0.1  | Initial| 首次发布        |

### 注意事项
- infer infer=true 走智能模式，infer=false 走简单模式。  
- OceanBase 仅在 db_provider=oceanbase 时生效；默认 sqlite。
- 使用 OceanBase 作为向量数据库的时候，需要确保数据库已经存在。
- seekdb作为 OceanBase 的轻量版，可以选择 db_provider=oceanbase，填写seekdb的连接信息就可以将seekdb作为向量数据库。
- 作用域 user_id/agent_id 会影响搜索/更新/删除范围，留空则不加作用域。  

### 贡献
- [PowerMem](https://github.com/oceanbase/powermem) 主仓库  
- [dify-plugin-powermem](https://github.com/oceanbase/dify-plugin-powermem) 插件仓库
