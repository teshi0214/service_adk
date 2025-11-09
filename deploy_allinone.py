"""Deploy ServiceNow Agent (All-in-one version) to Agent Engine."""

import os
import vertexai
from vertexai import agent_engines

# Set environment variables
os.environ["SERVICENOW_INSTANCE_URL"] = "https://dev349863.service-now.com"
os.environ["SERVICENOW_USERNAME"] = "admin"
os.environ["SERVICENOW_PASSWORD"] = "0214Teshi!"
os.environ["SERVICENOW_API_VERSION"] = "v1"
os.environ["SERVICENOW_KB_TABLE"] = "kb_knowledge"
os.environ["MAX_RESULTS"] = "100"
os.environ["REQUEST_TIMEOUT"] = "30"

# Import the agent
from agent_allinone import servicenow_agent

# GCP Configuration
PROJECT_ID = "agent-vi-473112"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://agent-test-0925"

print("🚀 Deploying ServiceNow Agent (All-in-one) to Agent Engine...")
print(f"   Project: {PROJECT_ID}")
print(f"   Location: {LOCATION}")
print(f"   Staging Bucket: {STAGING_BUCKET}")
print()

# Initialize client
client = vertexai.Client(project=PROJECT_ID, location=LOCATION)

# Create AdkApp
print("📦 Creating AdkApp...")
adk_app = agent_engines.AdkApp(agent=servicenow_agent)

# Environment variables for Agent Engine
env_vars = {
    "SERVICENOW_INSTANCE_URL": "https://dev349863.service-now.com",
    "SERVICENOW_USERNAME": "admin",
    "SERVICENOW_PASSWORD": "0214Teshi!",
    "SERVICENOW_API_VERSION": "v1",
    "SERVICENOW_KB_TABLE": "kb_knowledge",
    "MAX_RESULTS": "100",
    "REQUEST_TIMEOUT": "30",
}

# Deploy
print("🔨 Deploying to Agent Engine...")
try:
    remote_agent = client.agent_engines.create(
        agent=adk_app,
        config={
            "staging_bucket": STAGING_BUCKET,
            "requirements": [
                "google-cloud-aiplatform[agent_engines,adk]",
                "requests",
                "cloudpickle",
                "pydantic",
            ],
            "display_name": "ServiceNow KB Agent",
            "description": "ServiceNow Knowledge Base management agent",
            "env_vars": env_vars,
        }
    )
    
    print("\n✅ Deployment successful!")
    print(f"   Agent Resource Name: {remote_agent.api_resource.name}")
    print(f"\n📝 Save this for later use:")
    print(f"   {remote_agent.api_resource.name}")
    
except Exception as e:
    print(f"\n❌ Deployment failed: {e}")
    import traceback
    traceback.print_exc()
