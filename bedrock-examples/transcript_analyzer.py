import os

from boto3 import session
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

# Create boto3 session with manually defined credentials.
base_session = session.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", ""),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN", ""),
    region_name=os.getenv("AWS_REGION_NAME", "us-west-2"),
)

# Create a Bedrock Runtime client.
client = base_session.client("bedrock-runtime")

# Set the model ID, e.g. Palmyra X5.
# This is the ID for the cross-region inference profile for Palmyra X5.
# See https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html.
model_id = os.getenv("AWS_BEDROCK_MODEL_ID", "us.writer.palmyra-x5-v1:0")

# Load the document.
with open("../resources/meeting_transcript.md", "rb") as file:
    document_bytes = file.read()

# Start a conversation with a user message and the document.
conversation = [
    {
        "role": "user",
        "content": [
            {
                "text": "Create a summary of the meeting notes and provide a list of action items."
            },
            {
                "document": {
                    # Available formats: html, md, pdf, doc/docx, xls/xlsx, csv, and txt
                    "format": "md",
                    "name": "Meeting Transcript",
                    "source": {"bytes": document_bytes},
                }
            },
        ],
    }
]

try:
    # Send the message to the model.
    response = client.converse(
        modelId=model_id,
        messages=conversation,
        inferenceConfig={"maxTokens": 500, "temperature": 0.3},
    )

    # Extract and print the response text.
    response_text = response["output"]["message"]["content"][0]["text"]
    print(response_text)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)
