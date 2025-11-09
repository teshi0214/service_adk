"""ServiceNow API authentication utilities."""

import os
import base64
from typing import Dict


class ServiceNowAuth:
    """ServiceNow認証クラス (Basic Authentication)"""
    
    def __init__(
        self,
        instance_url: str,
        username: str,
        password: str
    ):
        self.instance_url = instance_url.rstrip('/')
        self.username = username
        self.password = password
    
    def get_headers(self) -> Dict[str, str]:
        """API呼び出し用のヘッダーを取得"""
        # Basic認証のための資格情報をエンコード
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        return {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }


def get_servicenow_client():
    """環境変数からServiceNowクライアントを作成"""
    auth = ServiceNowAuth(
        instance_url=os.getenv("SERVICENOW_INSTANCE_URL"),
        username=os.getenv("SERVICENOW_USERNAME"),
        password=os.getenv("SERVICENOW_PASSWORD")
    )
    return auth
