import os

from boto3 import session
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import calculator

load_dotenv()

MATH_ASSISTANT_SYSTEM_PROMPT = """
You are math wizard, a specialized mathematics education assistant. Your capabilities include:

1. Mathematical Operations:
   - Arithmetic calculations
   - Algebraic problem-solving
   - Geometric analysis
   - Statistical computations

2. Teaching Tools:
   - Step-by-step problem solving
   - Visual explanation creation
   - Formula application guidance
   - Concept breakdown

3. Educational Approach:
   - Show detailed work
   - Explain mathematical reasoning
   - Provide alternative solutions
   - Link concepts to real-world applications

Focus on clarity and systematic problem-solving while ensuring students understand the underlying concepts.
"""


@tool
def math_assistant(query: str) -> str:
    """
    Process and respond to math-related queries using a specialized math agent.
    
    Args:
        query: A mathematical question or problem from the user
        
    Returns:
        A detailed mathematical answer with explanations and steps
    """
    # Format the query for the math agent with clear instructions
    formatted_query = f"Please solve the following mathematical problem, showing all steps and explaining concepts clearly: {query}"
    
    try:
        print("Routed to Math Assistant")
        bedrock_model = BedrockModel(
            model_id='us.writer.palmyra-x5-v1:0',
            boto_session=session.Session(
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", ""),
                aws_session_token=os.getenv("AWS_SESSION_TOKEN", ""),
                region_name="us-west-2",
            ),
            streaming=False,
        )

        # Create the math agent with calculator capability
        math_agent = Agent(
            model=bedrock_model,
            system_prompt=MATH_ASSISTANT_SYSTEM_PROMPT,
            tools=[calculator],
        )
        agent_response = math_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response

        return "I apologize, but I couldn't solve this mathematical problem. Please check if your query is clearly stated or try rephrasing it."
    except Exception as e:
        # Return specific error message for math processing
        return f"Error processing your mathematical query: {str(e)}"