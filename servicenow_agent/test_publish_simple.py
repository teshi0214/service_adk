"""Simple test for publishing articles - hardcoded credentials."""

import base64
import requests

# Hardcoded credentials for testing
instance_url = "https://dev349863.service-now.com"
username = "admin"
password = "0214Teshi!"

# Encode credentials
credentials = f"{username}:{password}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

kb_table = "kb_knowledge"
api_url = f"{instance_url}/api/now/table/{kb_table}"

print("🔍 Test 1: Creating article in DRAFT state...")
create_data = {
    "short_description": "Test Article - Draft",
    "text": "This is a test article in draft state",
    "workflow_state": "draft"
}

response = requests.post(api_url, headers=headers, json=create_data, timeout=30)
print(f"Status: {response.status_code}")

if response.status_code == 201:
    result = response.json().get("result", {})
    sys_id = result.get("sys_id")
    number = result.get("number")
    print(f"✅ Created: {number} (sys_id: {sys_id})")
    
    # Test 2: Try to publish by updating
    print(f"\n🔍 Test 2: Publishing article {number}...")
    update_url = f"{api_url}/{sys_id}"
    update_data = {"workflow_state": "published"}
    
    response = requests.patch(update_url, headers=headers, json=update_data, timeout=30)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"✅ Published successfully!")
        result = response.json().get("result", {})
        print(f"   State: {result.get('workflow_state')}")
    else:
        print(f"❌ Failed to publish")
        print(f"   Response: {response.text}")
        
else:
    print(f"❌ Failed to create")
    print(f"   Response: {response.text}")

print("\n🔍 Test 3: Creating article DIRECTLY as PUBLISHED...")
create_data_published = {
    "short_description": "Test Article - Direct Publish",
    "text": "This article is created directly as published",
    "workflow_state": "published"
}

response = requests.post(api_url, headers=headers, json=create_data_published, timeout=30)
print(f"Status: {response.status_code}")

if response.status_code == 201:
    result = response.json().get("result", {})
    number = result.get("number")
    state = result.get("workflow_state")
    print(f"✅ Created: {number} with state: {state}")
else:
    print(f"❌ Failed")
    print(f"   Response: {response.text}")
