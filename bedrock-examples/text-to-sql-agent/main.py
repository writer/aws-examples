import json

from utils.agent import get_agent_alias_id_by_name, get_agent_id_by_name
from utils.config.aws_clients import bedrock_agent_client, bedrock_agent_runtime_client
from utils.config.constants import AGENT_ALIAS_NAME, AGENT_NAME


def invoke_text_to_sql(query, agent_id, agent_alias_id):
    agent_response = bedrock_agent_runtime_client.invoke_agent(
        inputText=query, agentId=agent_id, agentAliasId=agent_alias_id, sessionId="19"
    )

    for event in agent_response.get("completion"):
        if "chunk" in event:
            data = event["chunk"].get("bytes", b"No bytes in chunk!")
            print(data.decode("utf8"))

        elif "trace" in event:
            print(json.dumps(event["trace"], indent=2))
        else:
            print(f"Unexpected event: {event}")


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
