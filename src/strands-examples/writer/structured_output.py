import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel
from strands import Agent
from strands.models.writer import WriterModel

load_dotenv()


# Define a structured schema for creative content
class MarketingCampaign(BaseModel):
    campaign_name: str
    target_audience: str
    key_messages: List[str]
    call_to_action: str
    tone: str
    estimated_engagement: float


# Use Palmyra X5 for creative marketing content
model = WriterModel(
    client_args={"api_key": os.getenv("WRITER_API_KEY")},
    model_id="palmyra-x5",
    temperature=0.8,  # Higher temperature for creative output
)

agent = Agent(
    model=model,
    system_prompt="You are a creative marketing strategist. "
    "Generate innovative marketing campaigns with structured data.",
)

# Generate structured marketing campaign
response = agent.structured_output(
    output_model=MarketingCampaign,
    prompt="Create a marketing campaign for a new eco-friendly water bottle targeting young professionals aged 25-35.",
)

print(
    f"Campaign Name: {response.campaign_name}\n"
    f"Target Audience: {response.target_audience}\n"
    f"Key Messages: {response.key_messages}\n"
    f"Call to Action: {response.call_to_action}\n"
    f"Tone: {response.tone}\n"
    f"Estimated Engagement: {response.estimated_engagement}"
)
