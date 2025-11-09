"""Deploy ServiceNow Agent to Vertex AI Agent Engine."""

import os
import sys
import vertexai
from pathlib import Path

# Set environment variables before importing agent (to avoid warnings)
os.environ["SERVICENOW_INSTANCE_URL"] = "https://dev349863.service-now.com"
os.environ["SERVICENOW_USERNAME"] = "admin"
os.environ["SERVICENOW_PASSWORD"] = "0214Teshi!"
os.environ["SERVICENOW_API_VERSION"] = "v1"
os.environ["SERVICENOW_KB_TABLE"] = "kb_knowledge"
os.environ["MAX_RESULTS"] = "100"
os.environ["REQUEST_TIMEOUT"] = "30"

# Add agent to path
sys.path.insert(0, str(Path(__file__).parent))

from agent.agent import root_agent
from vertexai import agent_engines

# GCP Configuration
PROJECT_ID = "agent-vi-473112"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://agent-test-0925"

print("🚀 Deploying ServiceNow Agent to Agent Engine...")
print(f"   Project: {PROJECT_ID}")
print(f"   Location: {LOCATION}")
print(f"   Staging Bucket: {STAGING_BUCKET}")
print()

# Initialize Vertex AI client
client = vertexai.Client(
    project=PROJECT_ID,
    location=LOCATION,
)

# Create AdkApp
print("📦 Creating AdkApp...")
adk_app = agent_engines.AdkApp(agent=root_agent)

# Deploy to Agent Engine
print("🔨 Deploying to Agent Engine...")

# ServiceNow credentials - これは環境変数として設定する必要があります
env_vars = {
    "SERVICENOW_INSTANCE_URL": "https://dev349863.service-now.com",
    "SERVICENOW_USERNAME": "admin",
    "SERVICENOW_PASSWORD": "0214Teshi!",
    "SERVICENOW_API_VERSION": "v1",
    "SERVICENOW_KB_TABLE": "kb_knowledge",
    "MAX_RESULTS": "100",
    "REQUEST_TIMEOUT": "30",
}

try:
    remote_agent = client.agent_engines.create(
        agent=adk_app,
        config={
            "staging_bucket": STAGING_BUCKET,
            "requirements": [
                "google-cloud-aiplatform[agent_engines,adk]",
                "requests",
                "python-dotenv",
                "cloudpickle",
                "pydantic",
            ],
            "display_name": "ServiceNow Knowledge Base Agent",
            "description": "Agent for managing ServiceNow knowledge base articles",
            "env_vars": env_vars,  # 環境変数を追加
        }
    )
    
    print("\n✅ Deployment successful!")
    print(f"   Agent Resource Name: {remote_agent.api_resource.name}")
    print(f"\n📝 Save this resource name for future use:")
    print(f"   {remote_agent.api_resource.name}")
    
except Exception as e:
    print(f"\n❌ Deployment failed: {e}")
    import traceback
    traceback.print_exc()
