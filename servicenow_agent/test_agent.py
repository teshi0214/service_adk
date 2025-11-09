"""Test script for ServiceNow Knowledge Base Agent."""

import asyncio
from servicenow_agent import root_agent
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


async def test_search():
    """ナレッジ検索のテスト"""
    print("=== Test: Search Knowledge Base ===")
    
    runner = Runner(
        app_name="test_app",
        agent=root_agent,
        session_service=InMemorySessionService()
    )
    
    content = types.Content(
        role='user',
        parts=[types.Part(text="VPNに関する記事を検索して")]
    )
    
    async for event in runner.run_async(
        user_id="test_user",
        session_id="test_search",
        new_message=content
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
