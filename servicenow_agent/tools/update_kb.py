"""ServiceNow Knowledge Base update tool."""

import os
import requests
from typing import Dict, Any, Optional


def update_knowledge_article(
    sys_id: str,
    title: Optional[str] = None,
    content: Optional[str] = None,
    category: Optional[str] = None,
    state: Optional[str] = None
) -> Dict[str, Any]:
    """
    既存のナレッジ記事を更新する.
    
    Args:
        sys_id: 記事のシステムID
        title: 新しいタイトル(オプション)
        content: 新しい本文(オプション)
        category: 新しいカテゴリ(オプション)
        state: 新しい状態(draft/published/retired)(オプション)
        
    Returns:
        更新結果を含む辞書
    """
    from agent.auth import get_servicenow_client
    
    try:
        # ServiceNow認証クライアントを取得
        client = get_servicenow_client()
        
        # APIエンドポイント
        kb_table = os.getenv("SERVICENOW_KB_TABLE", "kb_knowledge")
        api_url = f"{client.instance_url}/api/now/table/{kb_table}/{sys_id}"
        
        # 更新データを構築
        update_data = {}
        
        if title is not None:
            update_data["short_description"] = title
        if content is not None:
            update_data["text"] = content
        if category is not None:
            update_data["kb_category"] = category
        if state is not None:
            update_data["workflow_state"] = state
        
        if not update_data:
            return {
                "success": False,
                "error": "No update data provided",
            }
        
        # API呼び出し
        response = requests.patch(
            api_url,
            headers=client.get_headers(),
            json=update_data,
            timeout=int(os.getenv("REQUEST_TIMEOUT", "30"))
        )
        
        if response.status_code == 200:
            data = response.json()
            result = data.get("result", {})
            
            return {
                "success": True,
                "sys_id": result.get("sys_id"),
                "number": result.get("number"),
                "title": result.get("short_description"),
                "state": result.get("workflow_state"),
                "updated_fields": list(update_data.keys()),
            }
        else:
            return {
                "success": False,
                "error": f"Failed to update article: {response.status_code}",
                "details": response.text,
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }
