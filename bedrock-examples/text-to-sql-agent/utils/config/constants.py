import os

from aws_clients import sts_client
from dotenv import load_dotenv

load_dotenv()

# Overall constants
ACCOUNT_ID = sts_client.get_caller_identity().get("Account")
AGENT_ALIAS_NAME = "sample-agent"
AGENT_NAME = "text-2-sql-agent"
REGION = os.getenv("AWS_REGION_NAME", "us-west-2")
SUFFIX = f"{REGION}-{ACCOUNT_ID}"
AGENT_ROLE_NAME = f"AmazonBedrockExecutionRoleForAgents_{SUFFIX}"
ACTION_GROUP_NAME = "QueryAthenaActionGroup"
AGENT_PROMPT = """You are an expert database querying assistant that can create simple and complex SQL queries to get
answers about baseball players.

Follow these instructions:
* First, you have to fetch the database schema by calling the /getschema endpoint.
* Then, based on the received schema, create an SQL query that calls the most relevant tables and fetches the most
relevant data from them. You have to generate the SQL query by converting the user's natural language request.
* After query creation, you have to call the /querydatabase endpoint and send the created SQL query as the request body.
This endpoint will return the query execution result.
* Format this result if needed and prepare a final answer for the user. It's important to include both the query
and execution results in the final answer.

Here is an example:
<example>
User Request: "Give me information about players with the top 3 highest salaries."

Assistant Action:
    * Calls /getschema endpoint
    * Receives schema showing tables:
        player (player_id, name, team_id)
        salary (player_id, season, salary)
    * Generates SQL:
        sql
            SELECT p.name AS player_name, s.salary
            FROM salaries s JOIN players p ON s.player_id = p.player_id
            ORDER BY s.salary DESC
            LIMIT 3
        sql
    * Calls /querydatabase with the above query
    * Receives results:
        player_name	 salary
        Mike Trout	 $37,116,000
        Gerrit Cole	 $36,000,000
        Max Scherzer $34,503,480
    * Final Answer:
        Here are the 3 highest-paid MLB players:

        sql
            SELECT p.name AS player_name, s.salary
            FROM salaries s JOIN players p ON s.player_id = p.player_id
            ORDER BY s.salary DESC
            LIMIT 3
        sql

        Query Results:
            Mike Trout - $37,116,000
            Gerrit Cole - $36,000,000
            Max Scherzer - $34,503,480
</example> """

# S3 constants
BEDROCK_AGENT_S3_ALLOW_POLICY_NAME = f"{AGENT_NAME}-s3-allow-{SUFFIX}"
BUCKET_NAME = f"{AGENT_NAME}-{SUFFIX}"
SCHEMA_KEY = f"{AGENT_NAME}-schema.json"

SCHEMA_ARN = f"arn:aws:s3:::{BUCKET_NAME}/{SCHEMA_KEY}"
SCHEMA_NAME = "text_to_sql_openai_schema.json"

S3_SCHEMA_PATH = f"{BUCKET_NAME}/{SCHEMA_KEY}"
S3_DATA_PATH = "data"
S3_GLUE_TARGET = f"s3://{BUCKET_NAME}/{S3_DATA_PATH}/TheHistoryofBaseball/"

# Bedrock constants
BEDROCK_AGENT_BEDROCK_ALLOW_POLICY_NAME = f"{AGENT_NAME}-allow-{SUFFIX}"
FOUNDATION_MODEL = os.getenv("AWS_BEDROCK_MODEL_ID", "us.writer.palmyra-x4-v1:0")
BEDROCK_POLICY_ARNS = [
    f"arn:aws:iam::{ACCOUNT_ID}:policy/{BEDROCK_AGENT_BEDROCK_ALLOW_POLICY_NAME}",
    f"arn:aws:iam::{ACCOUNT_ID}:policy/{BEDROCK_AGENT_S3_ALLOW_POLICY_NAME}",
]

# Glue constants
GLUE_CRAWLER_NAME = "TheHistoryOfBaseball"
GLUE_DATABASE_NAME = "thehistoryofbaseball"
GLUE_ROLE_NAME = "AWSGlueServiceRole"
GLUE_POLICY_ARNS = [
    "arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess",
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
]
DATA_PATH = "../../../resources/TheHistoryofBaseball/"
RESOURCES_PATH = "../../../resources/"

# Athena constants
ATHENA_RESULT_LOC = f"s3://{BUCKET_NAME}/athena_result/"

# Lambda constants
LAMBDA_CODE_PATH = "lambda_function.py"
LAMBDA_NAME = f"{AGENT_NAME}-{SUFFIX}"
LAMBDA_ROLE_NAME = f"{AGENT_NAME}-lambda-role-{SUFFIX}"
LAMBDA_POLICY_ARNS = [
    "arn:aws:iam::aws:policy/AmazonAthenaFullAccess",
    "arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess",
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
    "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole",
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
]
