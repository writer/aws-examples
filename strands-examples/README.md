# AWS Strands examples with WRITER models

This directory contains examples demonstrating how to use AWS Strands with WRITER's Palmyra family of models via different integration or AWS Bedrock.

## Table of contents

- [Overview](#overview)
- [Directory structure](#directory-structure)
  - [Writer - direct WRITER integration](#writer---direct-writer-integration)
  - [Bedrock - AWS Bedrock integration](#bedrock---aws-bedrock-integration)
- [Model information](#model-information)
  - [Available WRITER models](#available-writer-models)
  - [AWS Bedrock models (coming soon)](#aws-bedrock-models-coming-soon)
- [Resources](#resources)
- [Support](#support)

## Overview

AWS Strands is a framework for building AI agents and workflows. These examples showcase two different ways to integrate WRITER models with Strands:

- **`writer/`**: Direct integration using WRITER.
- **`bedrock/`**: Integration via AWS Bedrock (coming soon).

## Directory structure

### [`writer/` - direct WRITER integration](/strands-examples/writer/README.md)

Examples that use WRITER models directly through the WRITER with AWS Strands:

| Example | Description | Model used |
|---------|-------------|------------|
| **[Financial analysis](writer/README.md#financial-analysis-financial_analysispy)** | Analyze financial data and generate insights. | `palmyra-fin` |
| **[Vision image analysis](writer/README.md#vision-image-analysis-vision_image_analysispy)** | Analyze images and extract information. | `palmyra-x5` |
| **[Structured output](writer/README.md#structured-output-structured_outputpy)** | Generate structured data from unstructured text. | `palmyra-x5` |
| **[Long context](writer/README.md#long-context-long_contextpy)** | Handle long-form content and documents. | `palmyra-x5` |
| **[Enterprise workflow automation](writer/README.md#enterprise-workflow-automation-enterprise_workflow_automationpy)** | Automate enterprise workflows and processes. | `palmyra-x5` |
| **[Memory agent](writer/README.md#memory-agent-memory_agentpy)** | Agent with memory capabilities for conversation context. | `palmyra-x5` |
| **[Multi-agent examples](writer/README.md#multi-agent-examples-multi_agent_example)** | Collection of specialized AI assistants. | Various models |

#### Multi-agent examples

The `multi_agent_example/` directory contains specialized AI assistants:

| Example | Description | Model used |
|---------|-------------|------------|
| **[Creative Assistant](writer/multi_agent_example/creative_assistant.py)** | AI assistant for creative tasks and content generation. | `palmyra-creative` |
| **[Financial Assistant](writer/multi_agent_example/fin_assistant.py)** | AI assistant for financial analysis and insights. | `palmyra-fin` |
| **[Medical Assistant](writer/multi_agent_example/med_assistant.py)** | AI assistant for medical information and analysis. | `palmyra-med` |
| **[Knowledge Agent](writer/multi_agent_example/knowledge_agent.py)** | AI agent for knowledge management and retrieval. | `palmyra-x5` |

**Key features:**
- Direct integration access to full family of WRITER's Palmyra models.
- Real-time access to latest WRITER model capabilities.

### `bedrock/` - AWS Bedrock integration

Examples that use WRITER models through AWS Bedrock with Strands (coming soon).

**Key features:**
- Integration with AWS Bedrock infrastructure.
- Access to WRITER's Palmyra X4 and X5 models via AWS Bedrock.

## Model information

### [Available WRITER models](https://dev.writer.com/home/models)
- **`palmyra-x5`**: General purpose model with vision capabilities.
- **`palmyra-x4`**: Efficient general purpose model.
- **`palmyra-fin`**: Our finance domain specialized model.
- **`palmyra-creative`**: Specialized for creative thinking and writing.
- **`palmyra-med`**: Specialized for medical analysis.
- **`palmyra-vision`**: Designed for processing images.

### AWS Bedrock models (coming soon)
- **`writer.palmyra-x5-v1:0`**: Via AWS Bedrock US West (Oregon) with [cross-region inference support](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html).
- **`writer.palmyra-x4-v1:0`**: Via AWS Bedrock US West (Oregon) with [cross-region inference support](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html).

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
