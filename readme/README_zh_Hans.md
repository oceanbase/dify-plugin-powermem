## PowerMem [![PowerMem](https://img.shields.io/badge/PowerMem-blue)](https://www.powermem.ai/)

**Author:** oceanbase  
**Version:** 0.0.3  
**Type:** tool  

### 简介
- 封装 PowerMem SDK 的同步工具，适用于 Dify 工作流和 Agent 策略。
- 提供 8 个工具：add_memory / search_memories / update_memory / delete_all_memories / list_memories / get_profile / list_profiles / delete_profile。
- 返回 JSON（status/results/relations 等原样返回 SDK）+ text；时间为 ISO 字符串。

### 工具说明
1. **add_memory**：新增或智能合并记忆；messages（字符串或 JSON 列表/字典）、user_id/agent_id/run_id、metadata(JSON 字符串)、infer（默认 true）。启用用户画像时需提供 user_id，text 会显示 user_id 及画像摘要。  
2. **search_memories**：向量/混合检索记忆；query、user_id/agent_id/run_id、limit、threshold、filters(JSON 字符串)、add_profile（bool，包含画像需同时提供 user_id）。  
3. **update_memory**：按 memory_id 更新 content，可带 metadata。  
4. **delete_all_memories**：按 user_id/agent_id/run_id 范围删除全部。  
5. **list_memories**：列出记忆；filters(JSON 字符串)、limit/offset、user_id/agent_id/run_id。  
6. **get_profile**：按 user_id 获取用户画像（需启用用户画像且 OceanBase）。  
7. **list_profiles**：按主题过滤列出用户画像（需启用用户画像且 OceanBase）。  
8. **delete_profile**：按 user_id 删除用户画像（需启用用户画像且 OceanBase）。  

### 使用说明
1. 配置凭证：llm_provider（qwen/openai/硅基流动/deepseek，默认 qwen）、llm_api_key、llm_model（默认 qwen-plus）；embedder_provider（qwen/openai，默认 qwen）、embedder_api_key、embedder_model（默认 text-embedding-v4）、embedder_dims（默认 1536）；db_provider（默认 sqlite）。  
2. 如选 oceanbase，填写 host/port/user/password/database，并可选：graph_store_enabled（启用图谱，需 oceanbase），user_profile_enabled（启用用户画像，需 oceanbase）。  

### 版本历史
| 版本    | 日期       | 变更           |
|---------|-----------|----------------|
| v0.0.3  | 2026-01-06 | 使用 PowerMem 0.2.1 SDK，保留原始 JSON 返回，优化文本输出并新增用户画像工具 |
| v0.0.2  | 2025-12-17 | 优化工作流文本输出格式，增加ID等关键字段，使用PowerMem 0.2.0 SDK |
| v0.0.1  | Initial   | 首次发布        |

### 注意事项
- infer infer=true 走智能模式，infer=false 走简单模式。  
- OceanBase 仅在数据库类型为 oceanbase 时生效；默认 sqlite。
- 使用 OceanBase 作为向量数据库的时候，需要确保数据库已经存在。
- seekdb作为 OceanBase 的轻量版，可以选择数据库类型为 oceanbase，填写seekdb的连接信息就可以将seekdb作为向量数据库。
- 作用域 user_id/agent_id 等会影响搜索/更新/删除范围，留空则不加作用域。  
- 用户画像功能仅在 `user_profile_enabled=true` 且 `db_provider=oceanbase` 时可用；否则虽然相关工具显示可用但是画像相关工具会返回提示并不执行，search 的 `add_profile` 也不会返回画像。  
- 图谱功能（graph_store_enabled）仅在 `db_provider=oceanbase` 时可用，使用同一套 OceanBase 连接参数。

### 贡献
- [PowerMem](https://github.com/oceanbase/powermem) 主仓库  
- [dify-plugin-powermem](https://github.com/oceanbase/dify-plugin-powermem) 插件仓库
