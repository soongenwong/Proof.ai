import time
from google import genai
from google.genai import types

# Initialize client (loads GEMINI_API_KEY automatically)
client = genai.Client()

# Start video generation
operation = client.models.generate_videos(
    model="veo-2.0-generate-001",
    prompt="A golden retriever puppy playing with a red ball in a sunny garden, wide shot, soft light, cinematic",
    config=types.GenerateVideosConfig(
        person_generation="dont_allow",  # or "allow_adult"
        aspect_ratio="16:9"
    ),
)

# Poll until done
while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

# Download all generated videos
for idx, gen in enumerate(operation.response.generated_videos):
    client.files.download(file=gen.video)
    gen.video.save(f"video_{idx}.mp4")