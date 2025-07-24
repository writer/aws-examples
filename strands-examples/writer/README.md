# WRITER Strands Examples

This directory contains examples demonstrating how to use WRITER's Palmyra family of models with AWS Strands via direct integration. AWS Strands is a framework for building AI agents and workflows, and these examples showcase the full capabilities of WRITER's specialized and general-purpose models.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
  - [WRITER Account & API Access](#1-writer-account--api-access)
  - [Python Environment](#2-python-environment)
- [Installation & Setup](#installation--setup)
  - [Environment Configuration](#environment-configuration)
- [Examples](#examples)
  - [Financial Analysis](#financial-analysis-financial_analysispy)
  - [Vision Image Analysis](#vision-image-analysis-vision_image_analysispy)
  - [Structured Output](#structured-output-structured_outputpy)
  - [Long Context](#long-context-long_contextpy)
  - [Enterprise Workflow Automation](#enterprise-workflow-automation-enterprise_workflow_automationpy)
  - [Memory Agent](#memory-agent-memory_agentpy)
  - [Multi-Agent Examples](#multi-agent-examples-multi_agent_example)
- [Model Information](#model-information)
  - [Available WRITER Models](#available-writer-models)
- [Resources](#resources)
- [Support](#support)

## Overview

These examples showcase how to:
- **Financial Analysis**: Analyze financial data and generate insights using specialized finance models
- **Vision Image Analysis**: Process and analyze images with vision capabilities
- **Structured Output**: Generate structured data from unstructured text
- **Long Context**: Handle long-form content and documents
- **Enterprise Workflow Automation**: Automate enterprise workflows and processes
- **Memory Agent**: Create agents with conversation memory capabilities
- **Multi-Agent Collaboration**: Build specialized AI assistants for different domains

## Prerequisites

Before you begin, make sure you have:

- Python 3.10 or higher installed
- A [Writer AI Studio](https://app.writer.com/register) account
- A Writer API key. See instructions in the [API Quickstart](/home/quickstart)
- Basic familiarity with Python and [AWS Strands](https://strandsagents.com/latest/)

## Installation

To use Writer models with Strands Agents, install the optional Writer dependency:

```bash
pip install 'strands-agents[writer]'
```

**Note:** To follow along with the examples in this guide, you'll also need the [Strands Agent Tools package](https://github.com/strands-agents/tools). Install the package with `pip install strands-agents-tools`.

## Examples

### Financial Analysis (`financial_analysis.py`)

| Feature            | Description                                |
| ------------------ | ------------------------------------------ |
| **Tools Used**     | Financial data processing                   |
| **Complexity**     | Beginner                                   |
| **Agent Type**     | Single Agent                               |
| **Interaction**    | Command Line Interface                     |
| **Key Focus**      | Financial Data Analysis & Insights         |
| **Model Used**     | `palmyra-fin`                              |

**What it does:**
- Demonstrates the use of WRITER's specialized finance model
- Analyzes financial data and generates insights
- Shows domain-specific model capabilities

**Run the example:**
```bash
cd strands-examples/writer/
python financial_analysis.py
```

### Vision Image Analysis (`vision_image_analysis.py`)

| Feature            | Description                                |
| ------------------ | ------------------------------------------ |
| **Tools Used**     | Image processing and analysis               |
| **Complexity**     | Beginner                                   |
| **Agent Type**     | Single Agent                               |
| **Interaction**    | Command Line Interface                     |
| **Key Focus**      | Computer Vision & Image Understanding      |
| **Model Used**     | `palmyra-x5`                               |

**What it does:**
- Analyzes images using WRITER's vision capabilities
- Extracts information and insights from visual content
- Demonstrates multimodal AI capabilities

**Run the example:**
```bash
cd strands-examples/writer/
python vision_image_analysis.py
```

### Structured Output (`structured_output.py`)

| Feature            | Description                                |
| ------------------ | ------------------------------------------ |
| **Tools Used**     | Structured data generation                 |
| **Complexity**     | Beginner                                   |
| **Agent Type**     | Single Agent                               |
| **Interaction**    | Command Line Interface                     |
| **Key Focus**      | Data Extraction & Structured Output       |
| **Model Used**     | `palmyra-x5`                               |

**What it does:**
- Generates structured data from unstructured text
- Demonstrates WRITER's ability to format output in specific schemas
- Shows how to extract and organize information systematically

**Run the example:**
```bash
cd strands-examples/writer/
python structured_output.py
```

### Long Context (`long_context.py`)

| Feature            | Description                                |
| ------------------ | ------------------------------------------ |
| **Tools Used**     | Long document processing                   |
| **Complexity**     | Intermediate                               |
| **Agent Type**     | Single Agent                               |
| **Interaction**    | Command Line Interface                     |
| **Key Focus**      | Long-form Content Processing               |
| **Model Used**     | `palmyra-x5`                               |

**What it does:**
- Handles long-form content and documents
- Demonstrates WRITER's ability to process extended context
- Shows how to work with large documents and maintain context

**Run the example:**
```bash
cd strands-examples/writer/
python long_context.py
```

### Enterprise Workflow Automation (`enterprise_workflow_automation.py`)

| Feature            | Description                                |
| ------------------ | ------------------------------------------ |
| **Tools Used**     | Workflow automation                        |
| **Complexity**     | Intermediate                               |
| **Agent Type**     | Single Agent                               |
| **Interaction**    | Command Line Interface                     |
| **Key Focus**      | Business Process Automation                |
| **Model Used**     | `palmyra-x5`                               |

**What it does:**
- Automates enterprise workflows and processes
- Demonstrates how to integrate AI into business operations
- Shows practical applications for enterprise use cases

**Run the example:**
```bash
cd strands-examples/writer/
python enterprise_workflow_automation.py
```

### Memory Agent (`memory_agent.py`)

| Feature            | Description                                |
| ------------------ | ------------------------------------------ |
| **Tools Used**     | Conversation memory                        |
| **Complexity**     | Intermediate                               |
| **Agent Type**     | Single Agent with Memory                   |
| **Interaction**    | Command Line Interface                     |
| **Key Focus**      | Memory Operations & Contextual Responses   |
| **Model Used**     | `palmyra-x5`                               |

**What it does:**
- Creates agents with memory capabilities for conversation context
- Demonstrates how to maintain conversation state across interactions
- Shows how to build more engaging and contextual AI experiences

**Run the example:**
```bash
cd strands-examples/writer/
python memory_agent.py
```

### Multi-Agent Examples (`multi_agent_example/`)

| Feature            | Description                                |
| ------------------ | ------------------------------------------ |
| **Tools Used**     | calculator, python_repl, shell, http_request, editor, file operations |
| **Complexity**     | Intermediate                               |
| **Agent Type**     | Multi-Agent Architecture                   |
| **Interaction**    | Command Line Interface                     |
| **Key Focus**      | Dynamic Query Routing                      |
| **Models Used**    | `palmyra-x5`, `palmyra-fin`, `palmyra-med`, `palmyra-creative` |

**What it does:**
- Demonstrates multi-agent collaboration and specialization
- Shows how different agents can work together on complex tasks
- Illustrates domain-specific AI assistants

#### Available Multi-Agent Examples:

**Creative Assistant (`creative_assistant.py`)**
- **Model**: `palmyra-creative`
- **Purpose**: AI assistant for creative tasks and content generation
- **Use Cases**: Writing, brainstorming, creative problem-solving

**Financial Assistant (`fin_assistant.py`)**
- **Model**: `palmyra-fin`
- **Purpose**: AI assistant for financial analysis and insights
- **Use Cases**: Financial modeling, investment analysis, risk assessment

**Medical Assistant (`med_assistant.py`)**
- **Model**: `palmyra-med`
- **Purpose**: AI assistant for medical information and analysis
- **Use Cases**: Medical research, symptom analysis, healthcare insights

**Knowledge Agent (`knowledge_agent.py`)**
- **Model**: `palmyra-x5`
- **Purpose**: AI agent for knowledge management and retrieval
- **Use Cases**: Information organization, knowledge base management

**Run the examples:**
```bash
cd strands-examples/writer/multi_agent_example/
python creative_assistant.py
python fin_assistant.py
python med_assistant.py
python knowledge_agent.py
```

## Model Information

### Available WRITER Models

- **`palmyra-x5`**: General purpose model with vision capabilities
- **`palmyra-x4`**: Efficient general purpose model
- **`palmyra-fin`**: Finance domain specialized model
- **`palmyra-creative`**: Specialized for creative thinking and writing
- **`palmyra-med`**: Specialized for medical analysis
- **`palmyra-vision`**: Designed for processing images

For detailed model information, visit the [WRITER Models Documentation](https://dev.writer.com/home/models).

## Resources

- [WRITER API Documentation](https://dev.writer.com/)
- [AWS Strands Documentation](https://strandsagents.com/latest/)
- [WRITER Strands Integration Guide](https://dev.writer.com/home/integrations/strands)
- [Strands Agents GitHub](https://github.com/aws-samples/strands-agents)
- [WRITER Console](https://console.writer.com/)

## Support

For issues with:
- **WRITER Integration**: Check [WRITER Support](https://support.writer.com/)
- **AWS Strands**: Check [AWS Strands Documentation](https://docs.aws.amazon.com/strands/)
- **General Questions**: File an issue on this repository
