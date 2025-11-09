"""Test ServiceNow Basic authentication with multiple username patterns."""

import os
import sys
import base64
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent / "agent" / ".env")

import requests

# Get credentials
instance_url = os.getenv("SERVICENOW_INSTANCE_URL")
email = os.getenv("SERVICENOW_USERNAME")
password = os.getenv("SERVICENOW_PASSWORD")

print("🔍 Testing different username patterns...")
print(f"Instance URL: {instance_url}")
print(f"Email: {email}")
print(f"Password: {'*' * len(password) if password else 'NOT SET'}")
print()

# Try different username patterns
username_patterns = [
    ("Email", email),
    ("Admin", "admin"),
    ("Email prefix", email.split('@')[0] if email else None),
]

api_url = f"{instance_url}/api/now/table/kb_knowledge"
params = {"sysparm_limit": 1}

for pattern_name, username in username_patterns:
    if not username:
        continue
        
    print(f"🔐 Testing with {pattern_name}: {username}")
    
    # Encode credentials
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(api_url, headers=headers, params=params, timeout=30)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"\n✅ SUCCESS with {pattern_name}: {username}")
            print(f"   Update your .env file:")
            print(f"   SERVICENOW_USERNAME={username}")
            data = response.json()
            print(f"   Found {len(data.get('result', []))} articles")
            break
        else:
            print(f"   ❌ Failed: {response.json().get('error', {}).get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
