import uuid

from utils.agent import (
    format_agent_response,
    get_agent_alias_id_by_name,
    get_agent_id_by_name,
)
from utils.config.aws_clients import bedrock_agent_client, bedrock_agent_runtime_client
from utils.config.constants import AGENT_ALIAS_NAME, AGENT_NAME


def invoke_text_to_sql(query, agent_id, agent_alias_id):
    agent_response = bedrock_agent_runtime_client.invoke_agent(
        inputText=query,
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=str(uuid.uuid4()),
        enableTrace=True,
    )

    for event in agent_response.get("completion"):
        if formatted_response := format_agent_response(event):
            print(formatted_response)


if __name__ == "__main__":
    print("\n🧠 Text to SQL Agent 🧠\n")
    print("Options:")
    print("  'exit' - Exit the program")

    current_agent_id = get_agent_id_by_name(bedrock_agent_client, AGENT_NAME)
    current_agent_alias_id = get_agent_alias_id_by_name(
        bedrock_agent_client, current_agent_id, AGENT_ALIAS_NAME
    )

    while True:
        try:
            user_input = input("\n> ")

            if user_input.lower() == "exit":
                print("\nGoodbye! 👋")
                break

            invoke_text_to_sql(user_input, current_agent_id, current_agent_alias_id)

        except KeyboardInterrupt:
            print("\n\nExecution interrupted. Exiting.")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
