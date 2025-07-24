import json
import os

from ddgs import DDGS
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.writer import WriterModel

load_dotenv()


@tool
def web_search(query: str) -> str:
    """
    Function to research and collect more information to answer the query
    Args:
        query: The query that needs to be answered or more information needs to be collected.
    """
    try:
        results = DDGS().text(query=query, max_results=5)
        return "\n".join([json.dumps(result) for result in results])
    except Exception as e:
        return f"Failed to search. Error: {e}"


model = WriterModel(
    client_args={"api_key": os.getenv("WRITER_API_KEY")},
    model_id="palmyra-x5",
)

agent = Agent(
    model=model,
    tools=[web_search],
    system_prompt="You are an enterprise assistant that helps automate business workflows.",
)

response = agent("Research out Writer inc. the latest product")
