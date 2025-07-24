import os

from creative_assistant import creative_assistant
from dotenv import load_dotenv
from fin_assistant import fin_assistant
from med_assistant import med_assistant
from strands import Agent
from strands.models.writer import WriterModel

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

writer_model = WriterModel(
    client_args={"api_key": os.getenv("WRITER_API_KEY")}, model_id="palmyra-x5"
)

# Create a file-focused agent with selected tools
knowledge_agent = Agent(
    model=writer_model,
    system_prompt=KNOWLEDGE_AGENT_PROMPT,
    callback_handler=None,
    tools=[med_assistant, fin_assistant, creative_assistant],
)


if __name__ == "__main__":
    print("\n📁 Knowledge agent 📁\n")
    print(
        "Ask a question in medical, financial domains or question, that require extra creativity."
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
