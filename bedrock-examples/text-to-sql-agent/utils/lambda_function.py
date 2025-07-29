import os

import boto3

outputLocation = os.environ["OUTPUT_LOCATION"]


def get_schema():
    try:
        print("'/getschema' has called.")
        glue_client = boto3.client("glue")

        database_name = "thehistoryofbaseball"
        table_schema_list = []
        response = glue_client.get_tables(DatabaseName=database_name)

        table_names = [table.get("Name") for table in response.get("TableList", [])]

        for table_name in table_names:
            response = glue_client.get_table(
                DatabaseName=database_name, Name=table_name
            )
            columns = (
                response.get("Table", {})
                .get("StorageDescriptor", {})
                .get("Columns", [])
            )
            schema = {column.get("Name"): column.get("Type") for column in columns}
            table_schema_list.append({f"Table: {table_name}": f"Schema: {schema}"})

        return table_schema_list
    except Exception as e:
        error_message = f"Error in 'get_schema' handler occurred: {str(e)}"
        print(error_message)
        return error_message


def execute_athena_query(query):
    try:
        print("'/querydatabase' has called.")
        athena_client = boto3.client("athena")

        response = athena_client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={"Database": "thehistoryofbaseball"},
            ResultConfiguration={"OutputLocation": outputLocation},
        )

        query_execution_id = response.get("QueryExecutionId")
        print(f"Query Execution ID: {query_execution_id}")

        response_wait = athena_client.get_query_execution(
            QueryExecutionId=query_execution_id
        )

        while response_wait.get("QueryExecution", {}).get("Status", {}).get(
            "State", ""
        ) in ["QUEUED", "RUNNING"]:
            print("Query is still running.")
            response_wait = athena_client.get_query_execution(
                QueryExecutionId=query_execution_id
            )

        if (
            response_wait.get("QueryExecution", {}).get("Status", {}).get("State", "")
            == "SUCCEEDED"
        ):
            print("Query succeeded!")
            query_results = athena_client.get_query_results(
                QueryExecutionId=query_execution_id
            )
            extracted_output = extract_result_data(query_results)
            print(extracted_output)
            return extracted_output

        else:
            print(f"Query {query_execution_id} haven't reached 'SUCCEEDED' status.")
            return None
    except Exception as e:
        error_message = f"Error in 'execute_athena_query' handler occurred: {str(e)}\nExecution query: {query}"
        print(error_message)
        return error_message


def extract_result_data(query_results):
    result_data = []

    column_info = (
        query_results.get("ResultSet", {})
        .get("ResultSetMetadata", {})
        .get("ColumnInfo", [])
    )
    column_names = [column.get("Name") for column in column_info]

    for row in query_results.get("ResultSet", {}).get("Rows", [])[1:]:
        data = [item.get("VarCharValue") for item in row.get("Data", [])]
        result_data.append(dict(zip(column_names, data)))

    return result_data


def lambda_handler(event, context):
    result = None
    print("Lambda handler has called.")
    print("-" * 20 + "Input event" + "-" * 20)
    print(event)
    if event.get("apiPath", "") == "/getschema":
        result = get_schema()

    if event.get("apiPath", "") == "/querydatabase":
        properties = (
            event.get("requestBody", {})
            .get("content", {})
            .get("application/json", {})
            .get("properties", [])
        )

        if properties:
            query = properties[0].get("value")

            if query:
                result = execute_athena_query(query)

    if not result:
        print("Call failed.")
        result = f"Call failed. Received outcome: {result or 'empty result'}"

    api_response = {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": event.get("actionGroup"),
            "apiPath": event.get("apiPath"),
            "httpMethod": event.get("httpMethod"),
            "httpStatusCode": 200,
            "responseBody": {"application/json": {"body": str(result)}},
        },
        "sessionAttributes": event.get("sessionAttributes", {}),
        "promptSessionAttributes": event.get("promptSessionAttributes", {}),
    }

    return api_response
