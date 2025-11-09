"""ServiceNow Knowledge Base Agent."""

from google.adk import Agent

from . import prompt
from .settings import Settings

# Import tools from parent directory
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools import (
    search_knowledge_base,
    create_knowledge_article,
    update_knowledge_article,
    delete_knowledge_article,
)

# Model configuration
MODEL = "gemini-2.5-pro"

# Create the root agent
root_agent = Agent(
    name="servicenow_kb_agent",
    model=MODEL,
    description=(
        "A comprehensive ServiceNow Knowledge Base management agent "
        "that can search, create, update, and delete KB articles."
    ),
    instruction=prompt.SERVICENOW_KB_AGENT_PROMPT,
    tools=[
        search_knowledge_base,
        create_knowledge_article,
        update_knowledge_article,
        delete_knowledge_article,
    ],
)

# Load settings
settings = Settings()

# Validate settings on import
if not settings.validate():
    print("Warning: ServiceNow settings are not properly configured.")
    print("Please set the following environment variables:")
    print("- SERVICENOW_INSTANCE_URL")
    print("- SERVICENOW_CLIENT_ID")
    print("- SERVICENOW_CLIENT_SECRET")
    print("- SERVICENOW_USERNAME")
    print("- SERVICENOW_PASSWORD")
