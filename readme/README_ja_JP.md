## PowerMem [![PowerMem](https://img.shields.io/badge/PowerMem-blue)](https://www.powermem.ai/)

**Author:** oceanbase  
**Version:** 0.0.1  
**Type:** tool  

### 概要
- PowerMem SDK を同期ツールとして Dify ワークフロー／エージェントで利用するプラグインです。
- 提供ツール：add_memory / search_memories / update_memory / delete_all_memories / list_memories。
- 出力：JSON（status/results/relations）＋テキスト。日時は ISO 形式。

### ツール概要
1. **add_memory**：新規またはインテリジェント統合。messages（文字列または JSON 配列/オブジェクト）、user_id/agent_id/run_id、metadata(JSON 文字列)、infer（デフォルト true）。  
2. **search_memories**：ベクター／ハイブリッド検索。query、user_id/agent_id/run_id、limit、threshold、filters(JSON 文字列)。  
3. **update_memory**：memory_id（文字列入力、内部で int 変換）に対し content/metadata を更新。  
4. **delete_all_memories**：user_id/agent_id/run_id スコープで一括削除。  
5. **list_memories**：記憶の一覧。filters(JSON 文字列)、limit/offset、user_id/agent_id/run_id。  

### 使い方
1. 資格情報：llm_provider（デフォルト qwen）、llm_api_key、llm_model（デフォルト qwen-plus）；embedder_provider（デフォルト qwen）、embedder_api_key、embedder_model（デフォルト text-embedding-v4）；db_provider（デフォルト sqlite）。  
2. oceanbase を選ぶ場合、host/port/user/password/database を入力。  
3. LLM base_url：qwen は dashscope デフォルト、openai は https://api.openai.com/v1。  
4. 設定は `utils/config_builder.py` で生成（sqlite / oceanbase のみサポート）。  
5. ワークフローでツールを選択し、metadata/filters は有効な JSON 文字列で入力。  

### 注意事項
- infer=true はインテリジェントモード、infer=false はシンプルモード。  
- OceanBase は db_provider=oceanbase のときのみ有効。デフォルトは sqlite。  
- OceanBase をベクターストアとして使う場合、DB が既存であることを確認。  
- seekdb を軽量版として利用可能：db_provider=oceanbase を選び、seekdb の接続情報を入力すればベクターストアとして使用可能。  
- スコープ（user_id/agent_id）は検索/更新/削除範囲に影響。空の場合スコープなし。  

### バージョン履歴
| バージョン | 日付    | 変更内容        |
|-----------|--------|----------------|
| v0.0.1    | Initial| 最初のリリース  |

### コントリビューション
- [PowerMem](https://github.com/oceanbase/powermem) 本体リポジトリ  
- [dify-plugin-powermem](https://github.com/oceanbase/dify-plugin-powermem) プラグインリポジトリ
