"""ServiceNow Knowledge Base deletion tool."""

import os
import requests
from typing import Dict, Any, List


def delete_knowledge_article(
    sys_id: str
) -> Dict[str, Any]:
    """
    ナレッジ記事を削除する.
    
    Args:
        sys_id: 削除する記事のシステムID
        
    Returns:
        削除結果を含む辞書
    """
    from agent.auth import get_servicenow_client
    
    try:
        # ServiceNow認証クライアントを取得
        client = get_servicenow_client()
        
        # APIエンドポイント
        kb_table = os.getenv("SERVICENOW_KB_TABLE", "kb_knowledge")
        api_url = f"{client.instance_url}/api/now/table/{kb_table}/{sys_id}"
        
        # API呼び出し
        response = requests.delete(
            api_url,
            headers=client.get_headers(),
            timeout=int(os.getenv("REQUEST_TIMEOUT", "30"))
        )
        
        if response.status_code == 204:
            return {
                "success": True,
                "sys_id": sys_id,
                "message": "Article deleted successfully",
            }
        else:
            return {
                "success": False,
                "error": f"Failed to delete article: {response.status_code}",
                "details": response.text,
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }
