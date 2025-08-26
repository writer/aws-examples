import json
import os
import time
import zipfile
from io import BytesIO

from agent import get_agent_id_by_name
from config.aws_clients import (
    bedrock_agent_client,
    glue_client,
    iam_client,
    lambda_client,
    s3_client,
)
from config.constants import (
    ACCOUNT_ID,
    AGENT_ALIAS_NAME,
    AGENT_NAME,
    AGENT_PROMPT,
    AGENT_ROLE_NAME,
    ATHENA_RESULT_LOC,
    BEDROCK_AGENT_BEDROCK_ALLOW_POLICY_NAME,
    BEDROCK_AGENT_S3_ALLOW_POLICY_NAME,
    BEDROCK_POLICY_ARNS,
    BUCKET_NAME,
    DATA_PATH,
    FOUNDATION_MODEL,
    GLUE_CRAWLER_NAME,
    GLUE_DATABASE_NAME,
    GLUE_POLICY_ARNS,
    GLUE_ROLE_NAME,
    LAMBDA_CODE_PATH,
    LAMBDA_NAME,
    LAMBDA_POLICY_ARNS,
    LAMBDA_ROLE_NAME,
    REGION,
    RESOURCES_PATH,
    S3_DATA_PATH,
    S3_GLUE_TARGET,
    SCHEMA_ARN,
    SCHEMA_KEY,
    SCHEMA_NAME,
)


def create_bucket_and_upload_schema(
    s3_client, bucket_name, schema_name, bucket_key, region
):
    try:
        s3_client.create_bucket(
            Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": region}
        )
        print(f"Bucket {bucket_name} created successfully.")
    except Exception as e:
        print(f"Error creating bucket {bucket_name}:", e)

    try:
        s3_client.upload_file(schema_name, bucket_name, bucket_key)
        print(f"Schema {schema_name} uploaded successfully.")
    except Exception as e:
        print(f"Error {schema_name} uploading schema:", e)


def create_glue_db(glue_client, account_id, glue_db_name):
    try:
        glue_client.create_database(
            CatalogId=account_id,
            DatabaseInput={
                "Name": glue_db_name,
            },
        )
        print(f"Database {glue_db_name} created successfully.")
    except Exception as e:
        print(f"Error creating {glue_db_name} glue database:", e)


def start_crawler(glue_client, crawler_name):
    try:
        crawler = glue_client.get_crawler(Name=crawler_name)
        if crawler.get("Crawler", {}).get("State", "") == "READY":
            glue_client.start_crawler(Name=crawler_name)
            time.sleep(30)
            print(f"Crawler {crawler_name} started successfully.")
        else:
            time.sleep(30)
    except Exception as e:
        print(f"Error starting {crawler_name} crawler:", e)


def attach_role_policies(iam_client, role_name, policy_arns):
    try:
        for policy_arn in policy_arns:
            iam_client.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
        print(f"Policies {policy_arns} attached successfully to role {role_name}.")
    except Exception as e:
        print(f"Error attaching {policy_arns} policies to role {role_name}:", e)


def create_role(iam_client, role_name, role_policy):
    try:
        created_role = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(role_policy),
        )
        print(f"Role {role_name} created successfully.")
    except Exception as e:
        print(f"Error creating role {role_name}:", e)
        print("Trying to fetch it.")
        try:
            created_role = iam_client.get_role(RoleName=role_name)
            print(f"Role {role_name} fetched successfully.")
        except Exception as e:
            print(f"Error fetching role {role_name}:", e)
            created_role = {}

    return created_role


def create_policy(iam_client, policy_name, policy_document, policy_arn=None):
    try:
        policy = iam_client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document),
        )
        print(f"Policy {policy_name} created successfully.")
        return policy
    except Exception as e:
        print(f"Error creating policy {policy_name}:", e)
        print("Trying to fetch it.")
        try:
            policy = iam_client.get_policy(PolicyArn=policy_arn)
            print(f"Policy {policy_name} fetched successfully.")
        except Exception as e:
            print(f"Error fetching policy {policy_name}:", e)
            policy = {}

    return policy


def create_crawler(glue_client, crawler_name, role_name, s3_target):
    try:
        glue_client.create_crawler(
            Name=crawler_name,
            Role=role_name,
            DatabaseName="financialdata",
            Targets={
                "CatalogTargets": [],
                "DeltaTargets": [],
                "DynamoDBTargets": [],
                "HudiTargets": [],
                "IcebergTargets": [],
                "JdbcTargets": [],
                "MongoDBTargets": [],
                "S3Targets": [{"Exclusions": [], "Path": s3_target}],
            },
            Classifiers=[],
            Configuration='{"Version":1.0,"CreatePartitionIndex":true}',
            LakeFormationConfiguration={
                "AccountId": "",
                "UseLakeFormationCredentials": False,
            },
            RecrawlPolicy={"RecrawlBehavior": "CRAWL_EVERYTHING"},
            LineageConfiguration={"CrawlerLineageSettings": "DISABLE"},
        )
        print(f"Crawler {crawler_name} created successfully.")
    except Exception as e:
        print(f"Error creating crawler {crawler_name}:", e)


def upload_data(s3_client, s3_path, data_path, bucket_name):
    try:
        for root, _, files in os.walk(data_path):
            for filename in files:
                local_path = os.path.join(root, filename)
                path = os.path.join(
                    s3_path, str(os.path.relpath(str(local_path), RESOURCES_PATH))
                )
                s3_client.upload_file(local_path, bucket_name, path)

        print(f"Data uploaded to S3 bucket {bucket_name} successfully.")
    except Exception as e:
        print(f"Error uploading data to S3 bucket {bucket_name}:", e)


def create_lambda_function(
    lambda_client, lambda_function_name, lambda_role, athena_result_loc
):
    try:
        stream = BytesIO()
        with zipfile.ZipFile(stream, "w") as zip_file:
            zip_file.write(LAMBDA_CODE_PATH)
        zip_content = stream.getvalue()

        lambda_function = lambda_client.create_function(
            FunctionName=lambda_function_name,
            Runtime="python3.12",
            Timeout=180,
            Role=lambda_role.get("Role", {}).get("Arn"),
            Code={"ZipFile": zip_content},
            Handler="lambda_function.lambda_handler",
            Environment={"Variables": {"OUTPUT_LOCATION": athena_result_loc}},
        )

        print(f"Lambda function {lambda_function_name} created successfully.")
    except Exception as e:
        print(f"Error creating lambda {lambda_function_name}:", e)
        print("Trying to fetch it.")
        try:
            lambda_function = lambda_client.get_function(
                FunctionName=lambda_function_name
            )
            print(f"Lambda function {lambda_function_name} fetched successfully.")
        except Exception as e:
            print(f"Error fetching lambda {lambda_function_name}:", e)
            lambda_function = {}

    return lambda_function


def set_up_agent(bedrock_client, agent_name, model_name, agent_prompt, agent_resources):
    try:
        response = bedrock_client.create_agent(
            agentName=agent_name,
            agentResourceRoleArn=agent_resources.get("Role", {}).get("Arn"),
            description="Agent for performing SQL queries on financial data.",
            idleSessionTTLInSeconds=3600,
            foundationModel=model_name,
            instruction=agent_prompt,
        )

        print(f"Agent {agent_name} created successfully.")
        agent_id = response.get("agent", {}).get("agentId")
    except Exception as e:
        print(f"Error creating agent {agent_name}:", e)
        print("Trying to fetch it.")
        try:
            agent_id = get_agent_id_by_name(bedrock_client, agent_name)
        except Exception as e:
            print(f"Error fetching agent {agent_name}:", e)

    return agent_id


def create_action_group(
    bedrock_client, agent_id, group_executor, bucket_name, schema_key
):
    try:
        bedrock_client.create_agent_action_group(
            agentId=agent_id,
            agentVersion="DRAFT",
            actionGroupExecutor={"lambda": group_executor},
            actionGroupName="QueryAthenaActionGroup",
            apiSchema={"s3": {"s3BucketName": bucket_name, "s3ObjectKey": schema_key}},
            description="Actions for getting the database schema and querying the Athena database",
        )
        print("Action group created successfully.")
    except Exception as e:
        print("Error creating action group:", e)


def add_lambda_permission(lambda_client, lambda_name, region, account_id, agent_id):
    try:
        lambda_client.add_permission(
            FunctionName=lambda_name,
            StatementId="allow_bedrock",
            Action="lambda:InvokeFunction",
            Principal="bedrock.amazonaws.com",
            SourceArn=f"arn:aws:bedrock:{region}:{account_id}:agent/{agent_id}",
        )
        print(f"Permission {lambda_name} added successfully.")
    except Exception as e:
        print(f"Error adding lambda permission {lambda_name}:", e)


def prepare_agent(bedrock_client, agent_id, agent_alias_name):
    try:
        bedrock_client.prepare_agent(agentId=agent_id)
        time.sleep(20)
        print(f"Agent {agent_id} prepared successfully.")
        bedrock_client.create_agent_alias(
            agentId=agent_id, agentAliasName=agent_alias_name
        )

        print(f"Agent alias {agent_alias_name} created successfully.")
    except Exception as e:
        print(
            f"Error preparing agent {agent_id} and creating agent alias {agent_alias_name}:",
            e,
        )


# All time.sleep() executions are required for granting that AWS entities are finally/fully created
create_bucket_and_upload_schema(s3_client, BUCKET_NAME, SCHEMA_NAME, SCHEMA_KEY, REGION)
upload_data(s3_client, S3_DATA_PATH, DATA_PATH, BUCKET_NAME)

create_glue_db(glue_client, ACCOUNT_ID, GLUE_DATABASE_NAME)
create_role(
    iam_client,
    GLUE_ROLE_NAME,
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "sts:AssumeRole",
                "Principal": {"Service": "glue.amazonaws.com"},
            }
        ],
    },
)
attach_role_policies(iam_client, GLUE_ROLE_NAME, GLUE_POLICY_ARNS)
time.sleep(40)
create_crawler(glue_client, GLUE_CRAWLER_NAME, GLUE_ROLE_NAME, S3_GLUE_TARGET)
time.sleep(20)
start_crawler(glue_client, GLUE_CRAWLER_NAME)

lambda_role = create_role(
    iam_client,
    LAMBDA_ROLE_NAME,
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "sts:AssumeRole",
                "Principal": {"Service": "lambda.amazonaws.com"},
            }
        ],
    },
)
attach_role_policies(iam_client, LAMBDA_ROLE_NAME, LAMBDA_POLICY_ARNS)
time.sleep(40)
lambda_function = create_lambda_function(
    lambda_client, LAMBDA_NAME, lambda_role, ATHENA_RESULT_LOC
)


agent_bedrock_policy = create_policy(
    iam_client,
    BEDROCK_AGENT_BEDROCK_ALLOW_POLICY_NAME,
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["bedrock:InvokeModel*", "bedrock:CreateInferenceProfile"],
                "Resource": [
                    "arn:aws:bedrock:*::foundation-model/*",
                    "arn:aws:bedrock:*:*:inference-profile/*",
                    "arn:aws:bedrock:*:*:application-inference-profile/*",
                ],
            },
            {
                "Effect": "Allow",
                "Action": [
                    "bedrock:GetInferenceProfile",
                    "bedrock:ListInferenceProfiles",
                    "bedrock:DeleteInferenceProfile",
                    "bedrock:TagResource",
                    "bedrock:UntagResource",
                    "bedrock:ListTagsForResource",
                ],
                "Resource": [
                    "arn:aws:bedrock:*:*:inference-profile/*",
                    "arn:aws:bedrock:*:*:application-inference-profile/*",
                ],
            },
        ],
    },
    BEDROCK_POLICY_ARNS[0],
)
agent_s3_schema_policy = create_policy(
    iam_client,
    BEDROCK_AGENT_S3_ALLOW_POLICY_NAME,
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowAgentAccessOpenAPISchema",
                "Effect": "Allow",
                "Action": ["s3:GetObject"],
                "Resource": [SCHEMA_ARN],
            }
        ],
    },
    BEDROCK_POLICY_ARNS[1],
)
agent_role = create_role(
    iam_client,
    AGENT_ROLE_NAME,
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "bedrock.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }
        ],
    },
)
attach_role_policies(
    iam_client,
    AGENT_ROLE_NAME,
    [
        agent_bedrock_policy.get("Policy", {}).get("Arn"),
        agent_s3_schema_policy.get("Policy", {}).get("Arn"),
    ],
)
time.sleep(40)

agent_id = set_up_agent(
    bedrock_agent_client, AGENT_NAME, FOUNDATION_MODEL, AGENT_PROMPT, agent_role
)
time.sleep(20)
create_action_group(
    bedrock_agent_client,
    agent_id,
    lambda_function.get("FunctionArn", {}),
    BUCKET_NAME,
    SCHEMA_KEY,
)
add_lambda_permission(lambda_client, LAMBDA_NAME, REGION, ACCOUNT_ID, agent_id)
time.sleep(20)
prepare_agent(bedrock_agent_client, agent_id, AGENT_ALIAS_NAME)
