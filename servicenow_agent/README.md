# ServiceNow Knowledge Base Agent

ServiceNowのナレッジベースを管理するGoogle ADKエージェント

## 🎯 概要

このエージェントは、ServiceNowのナレッジベースに対して以下の操作を実行できます:

- **検索**: キーワードやカテゴリでナレッジ記事を検索
- **作成**: 新しいナレッジ記事を作成
- **更新**: 既存記事の内容やメタデータを更新
- **削除**: 不要な記事を削除

## 📁 プロジェクト構造

```
servicenow_agent/
├── __init__.py                 # パッケージ初期化
├── agent.py                    # メインエージェント定義
├── auth.py                     # ServiceNow認証処理
├── settings.py                 # 設定管理
├── prompt.py                   # プロンプト定義
├── .env                        # 環境変数設定
├── .gitignore                  # Git除外ファイル
├── requirements.txt            # Python依存関係
├── README.md                   # このファイル
└── tools/                      # ツール実装
    ├── __init__.py
    ├── search_kb.py            # ナレッジ検索
    ├── create_kb.py            # ナレッジ作成
    ├── update_kb.py            # ナレッジ更新
    └── delete_kb.py            # ナレッジ削除
```

## 🚀 セットアップ

### 1. 環境構築

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境のアクティベート
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 2. ServiceNow認証情報の取得

ServiceNowインスタンスで以下の情報を取得してください:

1. **OAuth 2.0 Application**の作成
   - ServiceNow管理画面 → System OAuth → Application Registry
   - "Create an OAuth API endpoint for external clients"を選択
   - Client IDとClient Secretを控える

2. **必要な権限**
   - Knowledge Management (kb_knowledge テーブルへのアクセス)
   - REST API アクセス権限

### 3. 環境変数の設定

`.env`ファイルを編集して、ServiceNow認証情報を設定:

```bash
SERVICENOW_INSTANCE_URL=https://your-instance.service-now.com
SERVICENOW_CLIENT_ID=your_client_id_here
SERVICENOW_CLIENT_SECRET=your_client_secret_here
SERVICENOW_USERNAME=your_username_here
SERVICENOW_PASSWORD=your_password_here
```

## 📖 使用方法

### 基本的な使い方

```python
from servicenow_agent import root_agent
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Runnerの作成
runner = Runner(
    app_name="servicenow_kb_app",
    agent=root_agent,
    session_service=InMemorySessionService()
)

# 検索例
async def search_example():
    content = types.Content(
        role='user',
        parts=[types.Part(text="VPN接続に関するナレッジ記事を検索して")]
    )
    
    async for event in runner.run_async(
        user_id="user123",
        session_id="session456",
        new_message=content
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"[{event.author}]: {part.text}")

# 作成例
async def create_example():
    content = types.Content(
        role='user',
        parts=[types.Part(text="""
新しいナレッジ記事を作成してください:
タイトル: VPN接続のトラブルシューティング
内容: VPN接続ができない場合の対処方法について説明します...
カテゴリ: ネットワーク
公開: はい
        """)]
    )
    
    async for event in runner.run_async(
        user_id="user123",
        session_id="session789",
        new_message=content
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"[{event.author}]: {part.text}")
```

## 🔧 利用可能なツール

### 1. search_knowledge_base

ナレッジベースを検索します。

**パラメータ:**
- `query` (str): 検索クエリ
- `category` (str): カテゴリでフィルタ(オプション)
- `limit` (int): 取得する最大件数(デフォルト: 10)

**例:**
```python
# エージェントに質問
"VPNに関する記事を検索して"
"ネットワークカテゴリの記事を5件取得して"
```

### 2. create_knowledge_article

新しいナレッジ記事を作成します。

**パラメータ:**
- `title` (str): 記事のタイトル
- `content` (str): 記事の本文
- `category` (str): カテゴリ(オプション)
- `publish` (bool): 作成後すぐに公開するか(デフォルト: False)

**例:**
```python
# エージェントに質問
"新規記事を作成: タイトル「テスト記事」、内容「これはテストです」"
```

### 3. update_knowledge_article

既存のナレッジ記事を更新します。

**パラメータ:**
- `sys_id` (str): 記事のシステムID
- `title` (str): 新しいタイトル(オプション)
- `content` (str): 新しい本文(オプション)
- `category` (str): 新しいカテゴリ(オプション)
- `state` (str): 新しい状態 draft/published/retired (オプション)

**例:**
```python
# エージェントに質問
"sys_id abc123 の記事のタイトルを「更新されたタイトル」に変更して"
"sys_id abc123 の記事を公開状態にして"
```

### 4. delete_knowledge_article

ナレッジ記事を削除します。

**パラメータ:**
- `sys_id` (str): 削除する記事のシステムID

**例:**
```python
# エージェントに質問
"sys_id abc123 の記事を削除して"
```

## 🔒 セキュリティ考慮事項

1. **認証情報の管理**
   - `.env`ファイルはGitにコミットしない(.gitignoreに追加済み)
   - 本番環境では環境変数またはシークレット管理サービスを使用
   - 定期的にClient SecretとPasswordを更新

2. **アクセス権限**
   - 最小権限の原則に従う
   - 必要なテーブルとAPIのみアクセス許可を付与
   - 削除権限は慎重に設定

3. **エラーハンドリング**
   - すべてのAPI呼び出しでタイムアウトを設定
   - 認証エラー時の適切な処理
   - リトライロジックの実装推奨

## 🧪 テスト

```python
# test_agent.py
import asyncio
from servicenow_agent import root_agent
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

async def test_search():
    """ナレッジ検索のテスト"""
    runner = Runner(
        app_name="test_app",
        agent=root_agent,
        session_service=InMemorySessionService()
    )
    
    content = types.Content(
        role='user',
        parts=[types.Part(text="VPNに関する記事を検索")]
    )
    
    async for event in runner.run_async(
        user_id="test_user",
        session_id="test_session",
        new_message=content
    ):
        if event.content:
            print(f"Response: {event.content}")

if __name__ == "__main__":
    asyncio.run(test_search())
```

## 📚 参考リンク

- [ServiceNow REST API Documentation](https://developer.servicenow.com/dev.do#!/reference/api/vancouver/rest/)
- [ServiceNow Knowledge Management API](https://docs.servicenow.com/bundle/vancouver-servicenow-platform/page/product/knowledge-management/reference/r_KnowledgeManagementAPI.html)
- [OAuth 2.0 in ServiceNow](https://docs.servicenow.com/bundle/vancouver-platform-security/page/administer/security/concept/c_OAuthApplications.html)
- [Google ADK Documentation](https://github.com/google/adk-python)

## 🛠️ トラブルシューティング

### 認証エラー

```
Error: Authentication failed: 401 Unauthorized
```

**解決方法:**
1. `.env`ファイルの認証情報が正しいか確認
2. ServiceNowでOAuth Applicationが正しく設定されているか確認
3. ユーザーに必要な権限が付与されているか確認

### APIエラー

```
Error: API request failed: 404 Not Found
```

**解決方法:**
1. `SERVICENOW_INSTANCE_URL`が正しいか確認
2. `SERVICENOW_KB_TABLE`の設定が正しいか確認
3. sys_idが正しく指定されているか確認

## 🤝 貢献

バグ報告や機能リクエストはIssueでお願いします。

## 📄 ライセンス

MIT License

## ✨ 機能拡張のアイデア

- [ ] ナレッジ記事のバッチ処理
- [ ] 添付ファイルのサポート
- [ ] 記事の履歴管理
- [ ] カテゴリの自動分類
- [ ] 記事の品質チェック
- [ ] 多言語サポート
- [ ] 記事のバージョン管理

---

作成者: Teshi  
作成日: 2025年11月
