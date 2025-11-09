"""Settings for ServiceNow KB Agent."""

import os
from typing import Dict


class Settings:
    """Configuration settings for the ServiceNow KB Agent."""
    
    def __init__(self):
        """Initialize settings from environment variables."""
        # ServiceNow認証情報
        self.instance_url = os.getenv("SERVICENOW_INSTANCE_URL")
        self.client_id = os.getenv("SERVICENOW_CLIENT_ID")
        self.client_secret = os.getenv("SERVICENOW_CLIENT_SECRET")
        self.username = os.getenv("SERVICENOW_USERNAME")
        self.password = os.getenv("SERVICENOW_PASSWORD")
        
        # API設定
        self.api_version = os.getenv("SERVICENOW_API_VERSION", "v1")
        self.kb_table = os.getenv("SERVICENOW_KB_TABLE", "kb_knowledge")
        self.max_results = int(os.getenv("MAX_RESULTS", "100"))
        
        # タイムアウト設定
        self.request_timeout = int(os.getenv("REQUEST_TIMEOUT", "30"))
    
    def to_env_dict(self) -> Dict[str, str]:
        """Convert settings to environment variable dictionary."""
        return {
            "SERVICENOW_INSTANCE_URL": self.instance_url,
            "SERVICENOW_CLIENT_ID": self.client_id,
            "SERVICENOW_CLIENT_SECRET": self.client_secret,
            "SERVICENOW_USERNAME": self.username,
            "SERVICENOW_PASSWORD": self.password,
            "SERVICENOW_API_VERSION": self.api_version,
            "SERVICENOW_KB_TABLE": self.kb_table,
            "MAX_RESULTS": str(self.max_results),
            "REQUEST_TIMEOUT": str(self.request_timeout),
        }
    
    def validate(self) -> bool:
        """Validate required settings."""
        required = [
            self.instance_url,
            self.client_id,
            self.client_secret,
            self.username,
            self.password
        ]
        return all(required)
