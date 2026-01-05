## PowerMem [![PowerMem](https://img.shields.io/badge/PowerMem-blue)](https://www.powermem.ai/)

**Author:** oceanbase  
**Version:** 0.0.3  
**Type:** tool  

### 概要
- PowerMem SDK を同期ツールとして Dify ワークフロー／エージェントで利用するプラグインです。
- 提供ツール：add_memory / search_memories / update_memory / delete_all_memories / list_memories / get_profile / list_profiles / delete_profile。
- 出力：JSON（status/results/relations など SDK からのレスポンスをそのまま返却）＋テキスト。日時は ISO 形式。

### ツール概要
1. **add_memory**：新規またはインテリジェント統合。messages（文字列または JSON 配列/オブジェクト）、user_id/agent_id/run_id、metadata(JSON 文字列)、infer（デフォルト true）。ユーザープロファイル有効時は user_id 必須、テキスト出力に user_id と画像要約を表示。  
2. **search_memories**：ベクター／ハイブリッド検索。query、user_id/agent_id/run_id、limit、threshold、filters(JSON 文字列)、add_profile（bool。画像を含めるには user_id も必須）。  
3. **update_memory**：memory_id に対し content/metadata を更新。  
4. **delete_all_memories**：user_id/agent_id/run_id スコープで一括削除。  
5. **list_memories**：記憶の一覧。filters(JSON 文字列)、limit/offset、user_id/agent_id/run_id。  
6. **get_profile**：user_id でユーザープロファイル取得（ユーザープロファイル有効かつ OceanBase 必須）。  
7. **list_profiles**：トピックフィルタでユーザープロファイル一覧（ユーザープロファイル有効かつ OceanBase 必須）。  
8. **delete_profile**：user_id でユーザープロファイル削除（ユーザープロファイル有効かつ OceanBase 必須）。  

### 使い方
1. 資格情報：llm_provider（デフォルト qwen）、llm_api_key、llm_model（デフォルト qwen-plus）；embedder_provider（デフォルト qwen）、embedder_api_key、embedder_model（デフォルト text-embedding-v4）；db_provider（デフォルト sqlite）。  
2. oceanbase を選ぶ場合、host/port/user/password/database を入力し、必要に応じて graph_store_enabled（グラフストア有効、OceanBase のみ）、user_profile_enabled（ユーザープロファイル有効、OceanBase のみ）を設定。

### 注意事項
- infer=true はインテリジェントモード、infer=false はシンプルモード。  
- OceanBase は db_provider=oceanbase のときのみ有効。デフォルトは sqlite。  
- OceanBase をベクターストアとして使う場合、DB が既存であることを確認。  
- seekdb を軽量版として利用可能：db_provider=oceanbase を選び、seekdb の接続情報を入力すればベクターストアとして使用可能。  
- スコープ（user_id/agent_id など）は検索/更新/削除範囲に影響。空の場合スコープなし。  
- ユーザープロファイル機能は `user_profile_enabled=true` かつ `db_provider=oceanbase` の場合のみ有効。満たさない場合、プロフィール関連ツールは実行せずエラーメッセージを返し、search の `add_profile` もプロフィールを返さない。  
- グラフ機能（graph_store_enabled）は `db_provider=oceanbase` の場合のみ有効で、同一の OceanBase 接続設定を使用。  

### バージョン履歴
| バージョン | 日付       | 変更内容        |
|-----------|-----------|----------------|
| v0.0.3    | 2026-01-06 | PowerMem 0.2.1 SDK、JSON を原文返却、テキスト出力改善＋ユーザープロファイルツール追加 |
| v0.0.2    | 2025-12-17 | ワークフローテキスト出力の改善、IDと主要フィールドを追加、PowerMem 0.2.0 SDK使用 |
| v0.0.1    | Initial   | 最初のリリース  |

### コントリビューション
- [PowerMem](https://github.com/oceanbase/powermem) 本体リポジトリ  
- [dify-plugin-powermem](https://github.com/oceanbase/dify-plugin-powermem) プラグインリポジトリ
