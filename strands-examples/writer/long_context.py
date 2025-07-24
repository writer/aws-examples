import os

from dotenv import load_dotenv
from strands import Agent
from strands.models.writer import WriterModel

load_dotenv()


# Use Palmyra X5 for processing very long documents
model = WriterModel(
    client_args={"api_key": os.getenv("WRITER_API_KEY")},
    model_id="palmyra-x5",
    temperature=0.2,
)

agent = Agent(
    model=model,
    system_prompt="You are a document analysis assistant that can process and summarize lengthy documents.",
)

# Can handle documents up to 1M tokens
# Replace the placeholder with your actual document content
actual_transcripts = """
[Meeting transcript content would go here - this could be thousands of lines of text
from meeting recordings, documents, or other long-form content that you want to analyze]
"""

response = agent(
    f"Summarize the key decisions and action items from these meeting transcripts: {actual_transcripts}"
)
