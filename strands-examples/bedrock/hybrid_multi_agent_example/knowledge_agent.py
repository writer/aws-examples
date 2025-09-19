#!/usr/bin/env python3
"""
# 📁 Knowledge Agent - Mixed Multi-Agent System

A specialized Strands agent that orchestrates specialized agents for medical, financial, and creative domains using Bedrock with WRITER models for orchestration, while sub-agents use direct WRITER API integration.

## What This Example Shows
- Multi-agent architecture using Bedrock with WRITER models
- Natural language routing to specialized domain agents
- Coordination between medical, financial, and creative assistants
- Using us.writer.palmyra-x5-v1:0 model for orchestration

## How to Run
1. Navigate to the example directory
2. Run: python knowledge_agent.py
3. Ask questions in medical, financial, or creative domains

## Example Queries
- "What are the symptoms of diabetes?" (Medical)
- "Explain the difference between traditional and Roth IRAs" (Financial)
- "Help me brainstorm ideas for a science fiction novel" (Creative)
"""
import os

from boto3 import session
from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel
from creative_assistant import creative_assistant
from fin_assistant import fin_assistant
from med_assistant import med_assistant

load_dotenv()

KNOWLEDGE_AGENT_PROMPT = """
You are KnowledgeAssistant, a sophisticated knowledge orchestrator designed
to coordinate knowledge support across different domains. Your role is to:

1. Analyze incoming user queries and determine the most appropriate specialized agent to handle them:
   - Med Agent: For answering medical questions
   - Fin Agent: For processing questions from financial domain
   - Creative Agent: For responding to questions that require extra creativity skills

2. Key Responsibilities:
   - Accurately classify user queries by domain area
   - Route requests to the appropriate specialized agent
   - Maintain context and coordinate multi-step problems
   - Ensure cohesive responses when multiple agents are needed

3. Decision Protocol:
   - If query involves terminology linked with human body, medicine, etc. → Med Agent
   - If query involves sets of data such stock, earnings, income, etc., phrases from financial domain, etc. → Fin Agent
   - If query processing requires some extra creativity: it linked with art, brainstorming, etc.  → Creative Agent

Always confirm your understanding before routing to ensure accurate assistance.
"""

bedrock_model = BedrockModel(
    model_id='us.writer.palmyra-x5-v1:0',
    boto_session=session.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", ""),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN", ""),
        region_name="us-west-2",
    ),
    streaming=False,
)

# Create a knowledge orchestrator agent with specialized tools
knowledge_agent = Agent(
    model=bedrock_model,
    system_prompt=KNOWLEDGE_AGENT_PROMPT,
    callback_handler=None,
    tools=[med_assistant, fin_assistant, creative_assistant],
)


if __name__ == "__main__":
    print("\n📁 Knowledge Agent - Bedrock Multi-Agent System 📁\n")
    print(
        "Ask a question in medical, financial domains, or questions that require extra creativity."
    )
    print("Type 'exit' to quit.")

    # Interactive loop
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == "exit":
                print("\nGoodbye! 👋")
                break

            response = knowledge_agent(
                user_input,
            )

            # Extract and print only the relevant content from the specialized agent's response
            content = str(response)
            print(content)

        except KeyboardInterrupt:
            print("\n\nExecution interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try asking a different question.")