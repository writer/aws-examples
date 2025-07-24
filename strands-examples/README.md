# AWS Strands examples with WRITER models

This directory contains examples demonstrating how to use AWS Strands with WRITER's Palmyra family of models via different integration or AWS Bedrock.

## Table of contents

- [Overview](#overview)
- [Directory structure](#directory-structure)
  - [Writer - direct WRITER integration](#writer---direct-writer-integration)
  - [Bedrock - AWS Bedrock integration](#bedrock---aws-bedrock-integration)
- [Prerequisites](#prerequisites)
  - [For WRITER direct integration](#for-writer-direct-integration-writer-folder)
  - [For AWS Bedrock integration](#for-aws-bedrock-integration-bedrock-folder)
- [Installation](#installation)
- [Model information](#model-information)
  - [Available WRITER models](#available-writer-models)
  - [AWS Bedrock models (coming soon)](#aws-bedrock-models-coming-soon)
- [Resources](#resources)
- [Support](#support)

## Overview

AWS Strands is a framework for building AI agents and workflows. These examples showcase two different ways to integrate WRITER models with Strands:

- **`writer/`**: Direct integration using WRITER
- **`bedrock/`**: Integration via AWS Bedrock (coming soon)

## Directory structure

### `writer/` - direct WRITER integration

Examples that use WRITER models directly through the WRITER with AWS Strands:

| Example | Description | Model used |
|---------|-------------|------------|
| **[Financial analysis](writer/financial_analysis.py)** | Analyze financial data and generate insights | `palmyra-fin` |
| **[Vision image analysis](writer/vision_image_analysis.py)** | Analyze images and extract information | `palmyra-x5` |
| **[Structured output](writer/structured_output.py)** | Generate structured data from unstructured text | `palmyra-x5` |
| **[Long context](writer/long_context.py)** | Handle long-form content and documents | `palmyra-x5` |
| **[Enterprise workflow automation](writer/enterpricse_workflow_automation.py)** | Automate enterprise workflows and processes | `palmyra-x5` |

**Key features:**
- Direct integration access to full family of WRITER's Palmyra models
- Real-time access to latest WRITER model capabilities

### `bedrock/` - AWS Bedrock integration

Examples that use WRITER models through AWS Bedrock with Strands (coming soon):

**Key features:**
- Integration with AWS Bedrock infrastructure
- Access to WRITER's Palmyra X4 and X5 models via AWS Bedrock

Before you begin, make sure you have:

- Python 3.10 or higher installed
- A [Writer AI Studio](https://app.writer.com/register) account
- A Writer API key. See instructions in the [API Quickstart](/home/quickstart)
- Basic familiarity with Python and [AWS Strands](https://strandsagents.com/latest/)

### For WRITER direct integration (`writer/` folder)
- **WRITER API key**: Get your API key from the [WRITER Console](https://console.writer.com/)

### For AWS Bedrock integration (`bedrock/` folder)
- **AWS account**: With access to Amazon Bedrock
- **Bedrock model access**: Subscribe to WRITER models in AWS Bedrock console (see below)
    #### Subscribe to Bedrock models
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

## Installation

1. **Install dependencies**
   ```bash
    pip install 'strands-agents[writer]'
    pip install strands-agents-tools
    ```
2. **Set up environment variables**

    If you haven't already, copy the `.env.template` file to a `.env` file in the **project root** with your credentials:
     ```
     cp .env.template .env
    ```
   ```bash
    # For WRITER direct integration
    WRITER_API_KEY=your_writer_api_key_here

    # For AWS Bedrock integration (when available)
    AWS_REGION_NAME=your AWS region
    AWS_BEDROCK_MODEL_ID=Bedrock model ID you want to use
    AWS_ACCESS_KEY_ID=your AWS access key
    AWS_SECRET_ACCESS_KEY=your AWS secret key
    AWS_SESSION_TOKEN=your AWS session token
   ```

## Model information

### [Available WRITER models](https://dev.writer.com/home/models)
- **`palmyra-x5`**: general purpose model with vision capabilities
- **`palmyra-x4`**: efficient general purpose model
- **`palmyra-fin`**: our finance domain specialized model
- **`palmyra-creative`**: specialized for creative thinking and writing
- **`palmyra-med`**: specialized for medical analysis
- **`palmyra-vision`**: designed for processing images

### AWS Bedrock models (coming soon)
- **`writer.palmyra-x5-v1:0`**: Via AWS Bedrock US West (Oregon) with [cross-region inference support](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)
- **`writer.palmyra-x4-v1:0`**: Via AWS Bedrock US West (Oregon) with [cross-region inference support](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)

## Resources

- [WRITER API documentation](https://dev.writer.com/)
- [AWS Bedrock documentation](https://docs.aws.amazon.com/bedrock/)
- [Strands agents GitHub](https://github.com/aws-samples/strands-agents)
- [Strands agents documentation](https://strandsagents.com/latest/)
- [WRITER Strands documentation](https://dev.writer.com/home/integrations/strands)
- [WRITER Bedrock documentation](https://dev.writer.com/home/integrations/instructor)

## Support

For issues with:
- **WRITER integration**: Check [WRITER support](https://support.writer.com/)
- **AWS Strands**: Check [AWS Strands documentation](https://docs.aws.amazon.com/strands/)
- **AWS Bedrock**: Check [AWS Bedrock documentation](https://docs.aws.amazon.com/bedrock/)
