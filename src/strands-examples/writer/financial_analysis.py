import os

from dotenv import load_dotenv
from strands import Agent
from strands.models.writer import WriterModel

load_dotenv()


# Use specialized finance model for financial analysis
model = WriterModel(
    client_args={"api_key": os.getenv("WRITER_API_KEY")}, model_id="palmyra-fin"
)

agent = Agent(
    model=model,
    system_prompt="You are a financial analyst assistant. Provide accurate, data-driven analysis.",
)

# Replace the placeholder with your actual financial report content
actual_report = """
[Your quarterly earnings report content would go here - this could include:
- Revenue figures
- Profit margins
- Growth metrics
- Risk factors
- Market analysis
- Any other financial data you want analyzed]
"""

response = agent(
    f"Analyze the key financial risks in this quarterly earnings report: {actual_report}"
)
