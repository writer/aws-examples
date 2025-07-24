# AWS Bedrock Examples with WRITER Models

This directory contains examples demonstrating how to use WRITER's Palmyra X4 and Palmyra X5 models on Amazon Bedrock. Amazon Bedrock is a fully managed service from AWS that enables developers to build and scale generative AI applications using foundation models from leading AI companies.

## Table of Contents

- [Directory structure](#directory-structure)
- [Prerequisites](#prerequisites)
  - [Installation & Setup](#installation--setup)
- [Examples](#examples)
  - [Transcript Analyzer](#transcript-analyzer-transcript_analyzerpy)
  - [Web Search Agent](#web-search-agent-web-search-agent)
- [Model Information](#model-information)
  - [Palmyra X5](#palmyra-x5-writerpalmyra-x5-v10)
  - [Palmyra X4](#palmyra-x4-writerpalmyra-x4-v10)
- [Resources](#resources)
- [Support](#support)

## Directory structure

### Examples that use WRITER models through AWS Bedrock:

| Example | Description | Model used |
|---------|-------------|------------|
| **[Transcript Analyzer](transcript_analyzer.py)** | Analyze meeting transcripts and extract summaries and action items. | `writer.palmyra-x5-v1:0` |
| **[Web Search Agent](web-search-agent/)** | Intelligent agent that can search the web and process information. | `writer.palmyra-x5-v1:0` |

**Key features:**
- Integration with AWS Bedrock infrastructure.
- Access to WRITER's Palmyra X5 and X4 model via AWS Bedrock.

## Prerequisites

Before running these examples, ensure you have:

### 1. AWS Account & Bedrock Access
- **AWS Account** with access to Amazon Bedrock.

### 2. Python Environment
- **Python 3.10+** installed.
- **boto3** SDK for Python: `pip install boto3`.

## Installation & setup

### Subscribe to Bedrock Models
Palmyra X5 and X4 models are available in the **US West (Oregon)** AWS Region with cross-Region inference.

1. Go to the [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Navigate to "Model access"
3. Request access to the Writer models you want to use:
   - `writer.palmyra-x5-v1:0`
   - `writer.palmyra-x4-v1:0`

### List Available Models
Verify your access to Palmyra models:
```bash
aws bedrock list-foundation-models --region=us-west-2 --by-provider writer --query "modelSummaries[*].modelId"
```

### Environment Configuration
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

## Examples

### Transcript Analyzer (`transcript_analyzer.py`)

| Feature            | Description                                |
| ------------------ | ------------------------------------------ |
| **Tools Used**     | Document processing                        |
| **Complexity**     | Beginner                                   |
| **Agent Type**     | Single Agent                               |
| **Interaction**    | Command Line Interface                     |
| **Key Focus**      | Document Processing & Summarization        |

**What it does:**
- Loads a meeting transcript from `../resources/meeting_transcript.md`.
- Sends it to WRITER LLM via AWS Bedrock for analysis.
- Returns a structured summary with action items.

**Run the example:**
1. Ensure your virtual environment is activated
2. Run `transcript_analyzer.py`
    ```bash
    cd src/bedrock-examples/
    python transcript_analyzer.py
    ```

### Web Search Agent (`web-search-agent/`)

| Feature            | Description                                |
| ------------------ | ------------------------------------------ |
| **Tools Used**     | web_search                                 |
| **Complexity**     | Beginner                                   |
| **Agent Type**     | Single Agent with Function Calling         |
| **Interaction**    | Command Line Interface                     |
| **Key Focus**      | Web Research & Contextual Responses        |

**What it does:**
- Performs web searches using function calling.
- Processes search results through the WRITER LLM via AWS Bedrock.
- Provides structured answers with citations and sources.

**File Structure:**
- **`main.py`**: Entry point that sets up the agent and initiates the conversation.
- **`agent.py`**: Core agent class that manages conversation flow, tool calling, and retry logic.
- **`tools.py`**: Defines the web search tool and AWS Bedrock tool configuration.

**Run the example:**
1. Ensure your virtual environment is activated
2. Run `main.py`
    ```bash
    cd src/bedrock-examples/web-search-agent
    python main.py
    ```

## Model Information

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
