import os

from agent import Agent
from boto3 import session
from dotenv import load_dotenv
from tools import tool_config

load_dotenv()

system_prompt = (
    "You are a researcher AI. Your task is to use the tools available to you and answer "
    "the user's query to the best of your capabilities. When you have final answer to "
    "the user's query then you are to strictly prefix it with FINAL ANSWER to stop the iterations."
)

# Create boto3 session with manually defined credentials.
base_session = session.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", ""),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN", ""),
    region_name=os.getenv("AWS_REGION_NAME", "us-west-2"),
)

# Create a Bedrock Runtime client.
client = base_session.client("bedrock-runtime")

researcher_agent = Agent(
    bedrock_client=client,
    model_id=os.getenv("AWS_BEDROCK_MODEL_ID", "us.writer.palmyra-x5-v1:0"),
    tool_config=tool_config,
    system_prompt=system_prompt,
)

output = researcher_agent.invoke("What is the GDP of India from 2009 to 2025")

print(output)
