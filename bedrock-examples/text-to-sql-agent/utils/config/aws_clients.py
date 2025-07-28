import os

from boto3 import session
from dotenv import load_dotenv

load_dotenv()

# Create boto3 session with manually defined credentials.
base_session = session.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", ""),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN", ""),
    region_name=os.getenv("AWS_REGION_NAME", "us-west-2"),
)

athena_client = base_session.client("athena")
bedrock_agent_client = base_session.client("bedrock-agent")
bedrock_agent_runtime_client = base_session.client("bedrock-agent-runtime")
glue_client = base_session.client("glue")
iam_client = base_session.client("iam")
s3_client = base_session.client("s3")
sts_client = base_session.client("sts")
lambda_client = base_session.client("lambda")
