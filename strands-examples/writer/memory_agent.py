import logging
import os

from dotenv import load_dotenv
from strands import Agent
from strands.models.writer import WriterModel
from strands_tools import mem0_memory, use_llm

logger = logging.getLogger(__name__)

# Load environment variables from .env file if it exists
load_dotenv()

# Set AWS credentials and configuration if you haven't specified then in .env file
# os.environ['OPENSEARCH_HOST'] = "your-opensearch-host.us-west-2.aoss.amazonaws.com"
# os.environ['AWS_ACCESS_KEY_ID'] = "your-aws-access-key-id"
# os.environ['AWS_SECRET_ACCESS_KEY'] = "your-aws-secret-access-key"
USER_ID = "example_user"

MEMORY_SYSTEM_PROMPT = f"""You are a personal assistant that maintains context by remembering user details.

Capabilities:
- Store new information using mem0_memory tool (action="store")
- Retrieve relevant memories (action="retrieve")
- List all memories (action="list")
- Provide personalized responses

Key Rules:
- Always include user_id={USER_ID} in tool calls
- Be conversational and natural in responses
- Format output clearly
- Acknowledge stored information
- Only share relevant information
- Politely indicate when information is unavailable
"""

writer_model = WriterModel(
    client_args={"api_key": os.getenv("WRITER_API_KEY")}, model_id="palmyra-x5"
)

# Create an agent with memory capabilities
memory_agent = Agent(
    model=writer_model,
    system_prompt=MEMORY_SYSTEM_PROMPT,
    tools=[mem0_memory, use_llm],
)


# Initialize some demo memories
def initialize_demo_memories():
    memory_agent.tool.mem0_memory(
        action="store",
        content=input("Please, provide any data I have to memorize! "),
        user_id=USER_ID,
    )


if __name__ == "__main__":
    print("\n🧠 Memory Agent 🧠\n")
    print("Options:")
    print("  'demo' - Initialize demo memories")
    print("  'exit' - Exit the program")
    print("\nOr try these examples:")
    print("  - What do you know about me?")
    print("  - Do I have any pets?")

    # Interactive loop
    while True:
        try:
            user_input = input("\n> ")

            if user_input.lower() == "exit":
                print("\nGoodbye! 👋")
                break
            elif user_input.lower() == "demo":
                initialize_demo_memories()
                print("\nDemo memories initialized!")
                continue

            # Call the memory agent
            memory_agent(user_input)

        except KeyboardInterrupt:
            print("\n\nExecution interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try a different request.")
