from agent import (
    get_action_group_id_by_name,
    get_agent_alias_id_by_name,
    get_agent_id_by_name,
)
from config.aws_clients import (
    bedrock_agent_client,
    glue_client,
    iam_client,
    lambda_client,
    s3_client,
)
from config.constants import (
    ACTION_GROUP_NAME,
    AGENT_ALIAS_NAME,
    AGENT_NAME,
    AGENT_ROLE_NAME,
    BEDROCK_AGENT_BEDROCK_ALLOW_POLICY_NAME,
    BEDROCK_AGENT_S3_ALLOW_POLICY_NAME,
    BEDROCK_POLICY_ARNS,
    BUCKET_NAME,
    GLUE_CRAWLER_NAME,
    GLUE_DATABASE_NAME,
    GLUE_POLICY_ARNS,
    GLUE_ROLE_NAME,
    LAMBDA_NAME,
    LAMBDA_POLICY_ARNS,
    LAMBDA_ROLE_NAME,
    SCHEMA_KEY,
)


def delete_glue_crawler(crawler_name):
    try:
        glue_client.delete_crawler(Name=crawler_name)
        print(f"Crawler {crawler_name} deleted successfully.")
    except Exception as e:
        print(f"Error deleting crawler {crawler_name} :", e)


def delete_glue_tables(database_name):
    try:
        response = glue_client.get_tables(DatabaseName=database_name)
        table_names_list = [
            table.get("Name") for table in response.get("TableList", [])
        ]
        glue_client.batch_delete_table(
            DatabaseName=database_name, TablesToDelete=table_names_list
        )

        print(f"Glue tables in {database_name} db were deleted successfully.")
    except Exception as e:
        print(f"Error deleting tables in database {database_name}:", e)


def delete_glue_database(database_name):
    try:
        glue_client.delete_database(Name=database_name)
        print(f"Database {database_name} deleted successfully.")
    except Exception as e:
        print(f"Error deleting {database_name} database:", e)


def clean_s3_bucket(bucket_name):
    try:
        objects = s3_client.list_objects(Bucket=bucket_name)
        s3_client.delete_objects(
            Bucket=bucket_name,
            Delete={
                "Objects": [
                    {"Key": obj.get("Key")} for obj in objects.get("Contents", [])
                ]
            },
        )
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} cleaned successfully.")
    except Exception as e:
        print(f"Error cleaning {bucket_name} bucket:", e)


def delete_agent_action_group(
    lambda_client,
    bedrock_client,
    agent_id,
    action_group_id,
    lambda_name,
    action_group_name,
    bucket_name,
    schema_key,
):
    try:
        function_arn = (
            lambda_client.get_function(FunctionName=lambda_name)
            .get("Configuration", {})
            .get("FunctionArn")
        )

        bedrock_client.update_agent_action_group(
            agentId=agent_id,
            agentVersion="DRAFT",
            actionGroupId=action_group_id,
            actionGroupName=action_group_name,
            actionGroupExecutor={"lambda": function_arn},
            apiSchema={"s3": {"s3BucketName": bucket_name, "s3ObjectKey": schema_key}},
            actionGroupState="DISABLED",
        )

        bedrock_client.delete_agent_action_group(
            agentId=agent_id, agentVersion="DRAFT", actionGroupId=action_group_id
        )
        print(f"Agent action group {action_group_name} deleted successfully.")
    except Exception as e:
        print(f"Error deleting agent action group {action_group_name}:", e)


def detach_role_policies(iam_client, policy_arns, role_name):
    try:
        for policy_arn in policy_arns:
            iam_client.detach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
        print(f"Policies {policy_arns} detached successfully from {role_name}.")
    except Exception as e:
        print(f"Error detaching policies from {role_name} role:", e)


def delete_roles(iam_client, role_names):
    try:
        for role_name in role_names:
            iam_client.delete_role(RoleName=role_name)
        print(f"Roles {role_names} deleted successfully.")
    except Exception as e:
        print(f"Error deleting {role_names} roles:", e)


def delete_policy_by_name(policy_name):
    paginator = iam_client.get_paginator("list_policies")
    for response in paginator.paginate(Scope="Local"):
        for policy in response.get("Policies", []):
            if policy.get("PolicyName", "") == policy_name:
                policy_arn = policy.get("Arn", "")
                try:
                    iam_client.delete_policy(PolicyArn=policy_arn)
                    print(f"Policy '{policy_name}' deleted successfully.")
                    return
                except Exception as e:
                    print(f"Error deleting policy '{policy_name}':", e)
                    return

    print(f"Policy '{policy_name}' not found.")


def delete_agent_alias(bedrock_agent, agent_id, agent_alias_id):
    try:
        bedrock_agent.delete_agent_alias(agentId=agent_id, agentAliasId=agent_alias_id)
        print(f"Agent alias {agent_alias_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting agent alias {agent_alias_id}:", e)


def delete_agent(bedrock_agent, agent_id):
    try:
        bedrock_agent.delete_agent(agentId=agent_id)
        print(f"Agent {agent_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting agent {agent_id}:", e)


def delete_lambda(lambda_client, lambda_name):
    try:
        lambda_client.delete_function(FunctionName=lambda_name)
        print(f"Lambda function {lambda_name} deleted successfully.")
    except Exception as e:
        print(f"Error deleting lambda function {lambda_name}:", e)


agent_id = get_agent_id_by_name(bedrock_agent_client, AGENT_NAME)
action_group_id = get_action_group_id_by_name(
    bedrock_agent_client, agent_id, ACTION_GROUP_NAME
)
agent_alias_id = get_agent_alias_id_by_name(
    bedrock_agent_client, agent_id, AGENT_ALIAS_NAME
)


delete_glue_crawler(GLUE_CRAWLER_NAME)
delete_glue_tables(GLUE_DATABASE_NAME)
delete_glue_database(GLUE_DATABASE_NAME)

delete_agent_action_group(
    lambda_client,
    bedrock_agent_client,
    agent_id,
    action_group_id,
    LAMBDA_NAME,
    ACTION_GROUP_NAME,
    BUCKET_NAME,
    SCHEMA_KEY,
)
delete_agent_alias(bedrock_agent_client, agent_id, agent_alias_id)
delete_agent(bedrock_agent_client, agent_id)

clean_s3_bucket(BUCKET_NAME)

delete_lambda(lambda_client, LAMBDA_NAME)

detach_role_policies(iam_client, LAMBDA_POLICY_ARNS, LAMBDA_ROLE_NAME)
detach_role_policies(iam_client, GLUE_POLICY_ARNS, GLUE_ROLE_NAME)
detach_role_policies(iam_client, BEDROCK_POLICY_ARNS, AGENT_ROLE_NAME)

delete_policy_by_name(BEDROCK_AGENT_BEDROCK_ALLOW_POLICY_NAME)
delete_policy_by_name(BEDROCK_AGENT_S3_ALLOW_POLICY_NAME)

delete_roles(iam_client, [AGENT_ROLE_NAME, LAMBDA_ROLE_NAME, GLUE_ROLE_NAME])
