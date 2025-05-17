# utils/agent_utils.py
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


def call_agent(agent: Agent, message_text: str) -> str:
    session_service = InMemorySessionService()
    session = session_service.create_session(
        app_name=agent.name, user_id="user1", session_id="session1"
    )
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
            for part in event.content.parts:
                if part.text is not None:
                    final_response += part.text
                    final_response += "\n"
    return final_response