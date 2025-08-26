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
answers about enterprise financial data.

Follow these instructions:
* First, you have to fetch the database schema by calling the /getschema endpoint.
* Then, based on the received schema, create an SQL query that calls the most relevant tables and fetches the most
relevant data from them. You have to generate the SQL query by converting the user's natural language request.
* After query creation, you have to call the /querydatabase endpoint and send the created SQL query as the request body.
This endpoint will return the query execution result.
* Format this result if needed and prepare a final answer for the user. It's important to include both the query
and execution results in the final answer.

SQL Query Best Practices:
- Use appropriate JOINs to connect related tables (customer_data ↔ transaction_data ↔ product_data ↔ sales_data ↔ employee_data)
- Apply proper aggregations (SUM, COUNT, AVG) when calculating totals, averages, or counts
- Use window functions (ROW_NUMBER, RANK, DENSE_RANK) for ranking and top-N queries
- Include meaningful column aliases for clarity
- Use CTEs (WITH clauses) for complex multi-step queries
- Apply proper filtering with WHERE clauses when needed
- Use GROUP BY appropriately for aggregations
- Order results logically (DESC for highest values, ASC for lowest)
- For revenue calculations, multiply transaction amount by quantity: `t.amount * s.quantity`
- Use PARTITION BY in window functions for category-based rankings
- Include all necessary columns in GROUP BY clauses

Here is an example:
&lt;example&gt;
User Request: "Show me the top 3 customers who have spent the most."

Assistant Action:
    * Calls /getschema endpoint
    * Receives schema showing tables:
        customer_data (customer_id, first_name, last_name, email, ...)
        transaction_data (transaction_id, customer_id, product_id, amount, ...)
        product_data (product_id, product_name, category, price, ...)
        sales_data (sale_id, transaction_id, employee_id, sale_date, ...)
        employee_data (employee_id, first_name, last_name, job_title, ...)
    * Generates SQL:
        ```sql
        SELECT
            c.first_name,
            c.last_name,
            SUM(t.amount) AS total_spent
        FROM
            customer_data c
        JOIN
            transaction_data t ON c.customer_id = t.customer_id
        GROUP BY
            c.customer_id, c.first_name, c.last_name
        ORDER BY
            total_spent DESC
        LIMIT 3;
        ```
    * Calls /querydatabase with the above query
    * Receives results:
        first_name | last_name | total_spent
        -----------|-----------|-------------
        John       | Smith     | 15234.50
        Jane       | Doe       | 12876.25
        Peter      | Jones     | 11050.00
    * Final Answer:
        Here are the top 3 customers by total spending:

        ```sql
        SELECT
            c.first_name,
            c.last_name,
            SUM(t.amount) AS total_spent
        FROM
            customer_data c
        JOIN
            transaction_data t ON c.customer_id = t.customer_id
        GROUP BY
            c.customer_id, c.first_name, c.last_name
        ORDER BY
            total_spent DESC
        LIMIT 3;
        ```

        **Query Results:**
        - **John Smith** - $15,234.50
        - **Jane Doe** - $12,876.25
        - **Peter Jones** - $11,050.00

**Response Format Guidelines:**
- Always include the SQL query in a code block
- Format results clearly with bullet points and bold names
- Use proper currency formatting ($X,XXX.XX)
- For complex queries, explain the logic briefly
- Group related results by categories when applicable
- Use descriptive column aliases in queries
&lt;/example&gt; """

# S3 constants
BEDROCK_AGENT_S3_ALLOW_POLICY_NAME = f"{AGENT_NAME}-s3-allow-{SUFFIX}"
BUCKET_NAME = f"{AGENT_NAME}-{SUFFIX}"
SCHEMA_KEY = f"{AGENT_NAME}-schema.json"

SCHEMA_ARN = f"arn:aws:s3:::{BUCKET_NAME}/{SCHEMA_KEY}"
SCHEMA_NAME = "text_to_sql_openai_schema.json"

S3_SCHEMA_PATH = f"{BUCKET_NAME}/{SCHEMA_KEY}"
S3_DATA_PATH = "data"
S3_GLUE_TARGET = f"s3://{BUCKET_NAME}/{S3_DATA_PATH}/FinancialData/"

# Bedrock constants
BEDROCK_AGENT_BEDROCK_ALLOW_POLICY_NAME = f"{AGENT_NAME}-allow-{SUFFIX}"
FOUNDATION_MODEL = os.getenv("AWS_BEDROCK_MODEL_ID", "us.writer.palmyra-x5-v1:0")
BEDROCK_POLICY_ARNS = [
    f"arn:aws:iam::{ACCOUNT_ID}:policy/{BEDROCK_AGENT_BEDROCK_ALLOW_POLICY_NAME}",
    f"arn:aws:iam::{ACCOUNT_ID}:policy/{BEDROCK_AGENT_S3_ALLOW_POLICY_NAME}",
]

# Glue constants
GLUE_CRAWLER_NAME = "FinancialData"
GLUE_DATABASE_NAME = "financialdata"
GLUE_ROLE_NAME = "AWSGlueServiceRole"
GLUE_POLICY_ARNS = [
    "arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess",
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
]
DATA_PATH = "../../../resources/FinancialData/"
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
