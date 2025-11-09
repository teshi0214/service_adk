"""ServiceNow Knowledge Base search tool."""

import os
import requests
from typing import Dict, Any, List


def search_knowledge_base(
    query: str = "",
    category: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """
    ServiceNowナレッジベースを検索する.
    
    Args:
        query: 検索クエリ文字列
        category: カテゴリでフィルタ(オプション)
        limit: 取得する最大件数(デフォルト: 10)
        
    Returns:
        検索結果を含む辞書
    """
    from agent.auth import get_servicenow_client
    
    try:
        # ServiceNow認証クライアントを取得
        client = get_servicenow_client()
        
        # APIエンドポイント
        kb_table = os.getenv("SERVICENOW_KB_TABLE", "kb_knowledge")
        api_url = f"{client.instance_url}/api/now/table/{kb_table}"
        
        # クエリパラメータ構築
        params = {
            "sysparm_limit": limit,
            "sysparm_fields": "sys_id,number,short_description,text,workflow_state,kb_category",
        }
        
        # 検索クエリの構築
        query_parts = []
        if query:
            query_parts.append(f"short_descriptionLIKE{query}^ORtextLIKE{query}")
        if category:
            query_parts.append(f"kb_category={category}")
        
        if query_parts:
            params["sysparm_query"] = "^".join(query_parts)
        
        # API呼び出し
        response = requests.get(
            api_url,
            headers=client.get_headers(),
            params=params,
            timeout=int(os.getenv("REQUEST_TIMEOUT", "30"))
        )
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get("result", [])
            
            # 結果をフォーマット
            formatted_articles = []
            for article in articles:
                formatted_articles.append({
                    "sys_id": article.get("sys_id"),
                    "number": article.get("number"),
                    "title": article.get("short_description"),
                    "content": article.get("text", "")[:200] + "...",  # 最初の200文字
                    "state": article.get("workflow_state"),
                    "category": article.get("kb_category"),
                })
            
            return {
                "success": True,
                "count": len(formatted_articles),
                "articles": formatted_articles,
                "query": query,
            }
        else:
            return {
                "success": False,
                "error": f"API request failed: {response.status_code}",
                "details": response.text,
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }
