"""ServiceNow Knowledge Base creation tool."""

import os
import requests
from typing import Dict, Any


def create_knowledge_article(
    title: str,
    content: str,
    category: str = "",
    publish: bool = False
) -> Dict[str, Any]:
    """
    新しいナレッジ記事を作成する.
    
    Args:
        title: 記事のタイトル
        content: 記事の本文
        category: カテゴリ(オプション)
        publish: 作成後すぐに公開するか(デフォルト: False)
        
    Returns:
        作成結果を含む辞書
    """
    from agent.auth import get_servicenow_client
    
    try:
        # ServiceNow認証クライアントを取得
        client = get_servicenow_client()
        
        # APIエンドポイント
        kb_table = os.getenv("SERVICENOW_KB_TABLE", "kb_knowledge")
        api_url = f"{client.instance_url}/api/now/table/{kb_table}"
        
        # 作成データを構築
        create_data = {
            "short_description": title,
            "text": content,
        }
        
        if category:
            create_data["kb_category"] = category
        
        # 公開状態を設定
        if publish:
            create_data["workflow_state"] = "published"
        else:
            create_data["workflow_state"] = "draft"
        
        # API呼び出し
        response = requests.post(
            api_url,
            headers=client.get_headers(),
            json=create_data,
            timeout=int(os.getenv("REQUEST_TIMEOUT", "30"))
        )
        
        if response.status_code == 201:
            data = response.json()
            result = data.get("result", {})
            
            return {
                "success": True,
                "sys_id": result.get("sys_id"),
                "number": result.get("number"),
                "title": result.get("short_description"),
                "state": result.get("workflow_state"),
                "url": f"{client.instance_url}/kb_view.do?sysparm_article={result.get('number')}",
            }
        else:
            return {
                "success": False,
                "error": f"Failed to create article: {response.status_code}",
                "details": response.text,
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }
