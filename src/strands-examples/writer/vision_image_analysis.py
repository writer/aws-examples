import os

from dotenv import load_dotenv
from strands import Agent
from strands.models.writer import WriterModel

load_dotenv()


# Use Palmyra X5 for vision tasks
model = WriterModel(
    client_args={"api_key": os.getenv("WRITER_API_KEY")}, model_id="palmyra-x5"
)

agent = Agent(
    model=model,
    system_prompt="You are a visual analysis assistant. Provide detailed, "
    "accurate descriptions of images and extract relevant information.",
)

# Read the image file
with open("../../resources/the_ninth_wave.jpg", "rb") as image_file:
    image_data = image_file.read()

messages = [
    {
        "role": "user",
        "content": [
            {"image": {"format": "png", "source": {"bytes": image_data}}},
            {
                "text": "Analyze this image and describe what you see. "
                "What are the key elements, colors, and any text or objects visible?"
            },
        ],
    }
]

# Create an agent with the image message
vision_agent = Agent(model=model, messages=messages)

# Analyze the image
response = vision_agent(
    "What are the main features of this image and what might it be used for?"
)

print(response)
