# Palmyra AWS Samples

This repository contains sample code demonstrating how to use AWS Bedrock and Strands with WRITER's Palmyra family of models

## Table of contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Examples](#examples)
  - [AWS Bedrock examples](#aws-bedrock-examples)
  - [WRITER Strands examples](#WRITER-strands-examples)
  - [Bedrock Strands examples (coming soon)](#bedrock-strands-examples)
- [About WRITER](#about-WRITER)
- [Support](#support)

## Overview
- **Bedrock examples**: examples of using WRITER's Palmyra X4 and X5 models with AWS Bedrock
- **WRITER Strands examples**: examples of using WRITER's family of Palmyra models via direct integration
- **(Coming soon) Bedrock Strands examples**: examples of using WRITER's X4 and X5 models via Bedrock in Strands

## Prerequisites

Before you begin, ensure you have the following:
- **Python 3.10** or higher installed

## Installation

1. Clone the Repository
    ```bash
    git clone <repository-url>
    cd palmyra-aws-samples
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
    Only fill this out if you're testing WRITER Strands examples
    ```
    WRITER_API_KEY=your WRITER API key
    ```
    ### AWS credentials
    Only fill this out if you're testing Bedrock-powered examples
    ```
    AWS_REGION_NAME=your AWS region
    AWS_BEDROCK_MODEL_ID=Bedrock model ID you want to use
    AWS_ACCESS_KEY_ID=your AWS access key
    AWS_SECRET_ACCESS_KEY=your AWS secret key
    AWS_SESSION_TOKEN=your AWS session token
    ```
    **Note:** You can find more information on how to  set up these credentials in the [Bedrock](/src/bedrock-examples/README.md) or [Strands](/src/strands-examples/README.md) examples README

## Examples

### AWS Bedrock Examples

Examples demonstrating how to use WRITER's Palmyra models with AWS Bedrock:

- **[Transcript Analyzer](src/bedrock-examples/README.md#transcript-analyzer-transcript_analyzerpy)**: Analyze meeting transcripts and extract summaries and action items
- **[Web Search Agent](src/bedrock-examples/README.md#web-search-agent-web-search-agent)**: Intelligent agent that can search the web and process information

### WRITER Strands Examples

Examples demonstrating how to use WRITER's models with AWS Strands via direct integration:

- **[Financial Analysis](src/strands-examples/WRITER/financial_analysis.py)**: Analyze financial data and generate insights
- **[Vision Image Analysis](src/strands-examples/WRITER/vision_image_analysis.py)**: Analyze images and extract information
- **[Structured Output](src/strands-examples/WRITER/structured_output.py)**: Generate structured data from unstructured text
- **[Long Context](src/strands-examples/WRITER/long_context.py)**: Handle long-form content and documents
- **[Enterprise Workflow Automation](src/strands-examples/WRITER/enterpricse_workflow_automation.py)**: Automate enterprise workflows and processes

### Bedrock Strands Examples

Examples demonstrating how to use WRITER's models with AWS Strands via Bedrock integration:

- **Coming Soon**: Examples will be added as they become available

## About WRITER

WRITER is the full-stack generative AI platform for enterprises. Quickly and easily build and deploy AI apps with a suite of developer tools fully integrated with our LLMs, graph-based RAG, AI guardrails, and more. To learn more, [visit our website](https://www.WRITER.com).

## Support

If you encounter any issues or have questions, please file an issue on this repository.