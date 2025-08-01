# Text-to-SQL agent

A powerful AWS Bedrock agent that converts natural language queries into SQL and executes them against a baseball database. This agent demonstrates how to build intelligent database querying assistants using AWS Bedrock's agent capabilities with WRITER's Palmyra models.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & setup](#installation--setup)
  - [Subscribe to Bedrock models](#subscribe-to-bedrock-models)
  - [List available models](#list-available-models)
  - [Environment configuration](#environment-configuration)
- [Usage](#usage)
  - [Interactive mode](#interactive-mode)
  - [Example queries](#example-queries)
- [Agent features](#agent-features)
  - [Trace mode](#trace-mode)
  - [Session management](#session-management)
- [Database schema](#database-schema)
- [Cleanup](#cleanup)
- [Model information](#model-information)
- [Resources](#resources)
- [Support](#support)

## Overview

This agent allows users to ask questions about baseball data in natural language, such as:
- "What player has the highest salary?"
- "Show me the top 10 players by batting average"
- "Which players won the most awards?"

The agent automatically:
1. Fetches the database schema
2. Converts your question into SQL
3. Executes the query against the database
4. Returns formatted results

### Architecture

The project consists of several AWS services working together:

- **AWS Bedrock Agent**: The main AI agent that handles natural language processing
- **AWS Lambda**: Executes SQL queries against the database
- **Amazon Athena**: Query engine for the baseball database
- **AWS Glue**: Data catalog and crawler for the baseball dataset
- **Amazon S3**: Stores the database schema and query results
- **IAM**: Manages permissions and roles

### Project structure

```
text-to-sql-agent/
├── main.py                          # Main application entry point
├── utils/
│   ├── agent.py                     # Agent utility functions
│   ├── clean.py                     # Cleanup utilities
│   ├── initialize_environment.py    # AWS resource setup
│   ├── lambda_function.py           # Lambda function for SQL execution
│   └── config/
│       ├── aws_clients.py           # AWS client configurations
│       └── constants.py             # Configuration constants
├── text_to_sql_openai_schema.json   # OpenAPI schema for the agent
└── README.md                        # This file
```

## Prerequisites

Before running these examples, ensure you have:

### 1. AWS account & Bedrock access
- **AWS Account** with access to Amazon Bedrock

### 2. Python environment
- **Python 3.10+** installed
- **boto3** SDK for Python: `pip install boto3`

## Installation & setup

### Subscribe to Bedrock models
Palmyra X5 and X4 models are available in the **US West (Oregon)** AWS Region with cross-Region inference.

1. Go to the [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Navigate to "Model access"
3. Request access to the Writer models you want to use:
   - `writer.palmyra-x5-v1:0`
   - `writer.palmyra-x4-v1:0`

### List available models
Verify your access to Palmyra models:
```bash
aws bedrock list-foundation-models --region=us-west-2 --by-provider writer --query "modelSummaries[*].modelId"
```

### Environment configuration
If you haven't already, copy the `.env.template` file to a `.env` file in the project root with your AWS credentials:
```
cp .env.template .env
```
**Note:** You only need to fill in the below credentials for these examples.

```
# AWS Credentials
AWS_REGION_NAME=your AWS region
AWS_BEDROCK_MODEL_ID=Bedrock model ID you want to use
AWS_ACCESS_KEY_ID=your AWS access key
AWS_SECRET_ACCESS_KEY=your AWS secret key
AWS_SESSION_TOKEN=your AWS session token
```

### Running `/text-to-sql`

#### 1. Initialize the environment

   Run the initialization script to create all required AWS resources:

   ```bash
   python utils/initialize_environment.py
   ```

   This script will:
   - Create an S3 bucket for storing data and results
   - Set up AWS Glue database and crawler for the baseball dataset
   - Create Lambda function for executing SQL queries
   - Create IAM roles and policies with appropriate permissions
   - Create the Bedrock agent with the specified foundation model
   - Set up action groups for database operations
   - Create an agent alias for deployment

**Note**: The initialization process may take 5-10 minutes as it creates multiple AWS resources and waits for them to be ready.

#### 2. Run the Agent

   Once initialization is complete, you can start using the agent:

   ```bash
   python main.py
   ```

## Usage

### Interactive mode

The agent runs in interactive mode by default. Simply type your questions:

```
🧠 Text to SQL Agent 🧠

Options:
  'exit' - Exit the program

> what player has the highest salary?
Calling LLM...
Trying to call /getschema...
Trying to call /querydatabase...
Final response were generated!

Here is the SQL query used to find the player with the highest salary:

sql
    SELECT p.name_first, p.name_last, s.salary 
    FROM salary s 
    JOIN player p ON s.player_id = p.player_id 
    ORDER BY s.salary DESC 
    LIMIT 1;

Query Result:
    Alex Rodriguez - $33,000,000

> exit
Goodbye! 👋
```

### Example queries

Try these example queries to test the agent:

- "Show me the top 5 players by salary"
- "Which players are in the Hall of Fame?"
- "What are the highest salaries by team?"
- "Show me players who won multiple awards"
- "What's the average salary by position?"

## Agent features

### Trace mode
The agent includes a trace mode that exposes the agent's "thinking" process in the console. Users can see the complete process of response creation, not just the final answer. This includes:
- LLM calls and responses
- Tool invocations (like `/getschema` and `/querydatabase`)
- Step-by-step reasoning

To enable/disable trace mode, modify the `enableTrace` parameter in the [`invoke_agent()` function call](main.py#L13) in `main.py`:

```python
agent_response = bedrock_agent_runtime_client.invoke_agent(
    inputText=query,
    agentId=agent_id,
    agentAliasId=agent_alias_id,
    sessionId=str(uuid.uuid4()),
    enableTrace=True,  # Set to False to disable trace mode
)
```

## Database schema

The agent works with a baseball database containing the following tables:

- **player**: Player information (ID, name, team, etc.)
- **salary**: Player salary data by season
- **hall_of_fame**: Hall of Fame inductees
- **player_award**: Awards won by players
- **player_award_vote**: Award voting details

**Note:** The baseball database is located in the `\resources` folder

## Cleanup

To remove all created resources:

```bash
python utils/clean.py
```

This will delete:
- The Bedrock agent and alias
- Lambda function
- S3 bucket and contents
- IAM roles and policies
- Glue database and crawler

## Model information

### Palmyra X5 (`writer.palmyra-x5-v1:0`)
- **Model ID**: `us.writer.palmyra-x5-v1:0`
- **Region**: US West (Oregon) with [cross-region inference support](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)

### Palmyra X4 (`writer.palmyra-x4-v1:0`)
- **Model ID**: `writer.palmyra-x4-v1:0`
- **Region**: US West (Oregon) with [cross-region inference support](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)

## Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [WRITER Bedrock Integration Guide](https://dev.writer.com/home/integrations/bedrock)
- [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
- [boto3 Bedrock Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)

## Support

For issues with:
- **WRITER Integration**: Check [WRITER Support](https://support.writer.com/)
- **AWS Bedrock**: Check [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)