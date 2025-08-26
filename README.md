# AWS Examples

This repository contains sample code demonstrating how to use AWS Bedrock and Strands with WRITER's Palmyra family of models.

## Table of contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Examples](#examples)
  - [AWS Bedrock examples](#aws-bedrock-examples)
  - [WRITER Strands examples](#writer-strands-examples)
  - [Bedrock Strands examples (coming soon)](#bedrock-strands-examples)
- [Resources](#resources)
- [About WRITER](#about-writer)
- [Support](#support)

## Overview
- **Bedrock examples**: Examples of using WRITER's Palmyra X4 and X5 models with AWS Bedrock.
- **WRITER Strands examples**: Examples of using WRITER's family of Palmyra models via direct integration.
- **(Coming soon) Bedrock Strands examples**: Examples of using WRITER's X4 and X5 models via Bedrock in Strands.

## Prerequisites

Before you begin, ensure you have the following:
- **Python 3.10** or higher installed.

## Installation

1. Clone the Repository
    ```bash
    git clone https://github.com/writer/aws-examples.git
    cd aws-examples
    ```
2. Create and activate a virtual environment:
   ```
   python -m venv my_env
   source my_env/bin/activate  # On Windows, use `my_env\Scripts\activate`
    ```

3. Set Up Environment Variables

    Copy the `.env.template` file to a `.env` file in the project root with your credentials:

    ```
    cp .env.template .env
    ```

    ### WRITER credentials
    Only fill this out if you're testing WRITER Strands examples.
    ```
    WRITER_API_KEY=your WRITER API key
    ```
    ### AWS credentials
    Only fill this out if you're testing Bedrock-powered examples.
    ```
    AWS_REGION_NAME=your AWS region
    AWS_BEDROCK_MODEL_ID=Bedrock model ID you want to use
    AWS_ACCESS_KEY_ID=your AWS access key
    AWS_SECRET_ACCESS_KEY=your AWS secret key
    AWS_SESSION_TOKEN=your AWS session token
    ```
    **Note:** You can find more information on how to set up these credentials in the [Bedrock](/bedrock-examples/README.md) or [Strands](/strands-examples/README.md) examples README.

## Examples

### [AWS Bedrock Examples](bedrock-examples/README.md)

Examples demonstrating how to use WRITER's Palmyra models with AWS Bedrock:

- **[Transcript Analyzer](bedrock-examples/README.md#transcript-analyzer-transcript_analyzerpy)**: Analyze meeting transcripts and extract summaries and action items.
- **[Web Search Agent](bedrock-examples/README.md#web-search-agent-web-search-agent)**: Intelligent agent that can search the web and process information.

### [WRITER Strands Examples](strands-examples/writer/README.md)

Examples demonstrating how to use WRITER's models with AWS Strands via direct integration:

- **[Financial Analysis](strands-examples/writer/README.md#financial-analysis-financial_analysispy)**: Analyze financial data and generate insights.
- **[Vision Image Analysis](strands-examples/writer/README.md#vision-image-analysis-vision_image_analysispy)**: Analyze images and extract information.
- **[Structured Output](strands-examples/writer/README.md#structured-output-structured_outputpy)**: Generate structured data from unstructured text.
- **[Long Context](strands-examples/writer/README.md#long-context-long_contextpy)**: Handle long-form content and documents.
- **[Enterprise Workflow Automation](strands-examples/writer/README.md#enterprise-workflow-automation-enterprise_workflow_automationpy)**: Automate enterprise workflows and processes.
- **[Memory Agent](strands-examples/writer/README.md#memory-agent-memory_agentpy)**: Agent with memory capabilities for conversation context.
- **[Multi-Agent Examples](strands-examples/writer/README.md#multi-agent-examples-multi_agent_example)**:
  - [Creative Assistant](strands-examples/writer/multi_agent_example/creative_assistant.py): AI assistant for creative tasks.
  - [Financial Assistant](strands-examples/writer/multi_agent_example/fin_assistant.py): AI assistant for financial analysis.
  - [Medical Assistant](strands-examples/writer/multi_agent_example/med_assistant.py): AI assistant for medical information.
  - [Knowledge Agent](strands-examples/writer/multi_agent_example/knowledge_agent.py): AI agent for knowledge management.

### Bedrock Strands Examples

Examples demonstrating how to use WRITER's models with AWS Strands via Bedrock integration:

- **Coming Soon**: Examples will be added as they become available.

## Resources

The `resources/` directory contains sample data and files used by the examples:

- **[Meeting Transcript](resources/meeting_transcript.md)**: Sample meeting transcript for testing the transcript analyzer.
- **[The Ninth Wave](resources/the_ninth_wave.jpg)**: Sample image for testing vision analysis capabilities.
- **[Financial Data](resources/FinancialData/)**: Sample enterprise financial dataset for testing database querying capabilities.

## About WRITER

WRITER is the full-stack generative AI platform for enterprises. Quickly and easily build and deploy AI apps with a suite of developer tools fully integrated with our LLMs, graph-based RAG, AI guardrails, and more. To learn more, [visit our website](https://www.WRITER.com).

## Support

If you encounter any issues or have questions, please file an issue on this repository.
