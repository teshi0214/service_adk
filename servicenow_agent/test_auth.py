"""Test ServiceNow authentication."""

import os
import sys
from pathlib import Path

# Add agent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables from agent/.env
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / "agent" / ".env")

import requests

# Get credentials from environment
instance_url = os.getenv("SERVICENOW_INSTANCE_URL")
client_id = os.getenv("SERVICENOW_CLIENT_ID")
client_secret = os.getenv("SERVICENOW_CLIENT_SECRET")
username = os.getenv("SERVICENOW_USERNAME")
password = os.getenv("SERVICENOW_PASSWORD")

print("🔍 Checking environment variables...")
print(f"Instance URL: {instance_url}")
print(f"Client ID: {client_id}")
print(f"Client Secret: {'*' * len(client_secret) if client_secret else 'NOT SET'}")
print(f"Username: {username}")
print(f"Password: {'*' * len(password) if password else 'NOT SET'}")
print()

# Test OAuth authentication
print("🔐 Testing OAuth authentication...")
token_url = f"{instance_url}/oauth_token.do"

payload = {
    "grant_type": "password",
    "client_id": client_id,
    "client_secret": client_secret,
    "username": username,
    "password": password
}

try:
    response = requests.post(token_url, data=payload, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ Authentication successful!")
        print(f"Access Token: {data.get('access_token')[:20]}...")
        print(f"Token Type: {data.get('token_type')}")
    else:
        print("\n❌ Authentication failed!")
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
