"""Video generation tool using Gemini API."""

from typing import Annotated
from pydantic import BaseModel, Field

from google import genai
from google.genai import types
import asyncio

import uuid
import os

class Output(BaseModel):
    """Response from the video generation tool."""
    success: bool
    message: str
    task_id: str | None = None  # Add a task_id for tracking

async def _background_generate_video(task_id, prompt, aspect_ratio, person_generation):
    try:
        client = genai.Client(api_key="")
        operation = client.models.generate_videos(
            model="veo-2.0-generate-001",
            prompt=prompt,
            config=types.GenerateVideosConfig(
                person_generation=person_generation,
                aspect_ratio=aspect_ratio,
            ),
        )
        while not operation.done:
            print(f"[{task_id}] Waiting for video generation to complete, 10 more seconds...")
            await asyncio.sleep(10)
            operation = client.operations.get(operation)
        for idx, gen in enumerate(operation.response.generated_videos):
            print(f"[{task_id}] Downloading video {idx + 1}/{len(operation.response.generated_videos)}...")
            filename = f"video_{task_id}_{idx}.mp4"
            client.files.download(file=gen.video)
            gen.video.save(filename)
        print(f"[{task_id}] Video generation completed.")
    except Exception as e:
        print(f"[{task_id}] Video generation failed: {str(e)}")

async def generate_video(
    prompt: Annotated[
        str, Field(description="Text prompt describing the video to generate", min_length=5)
    ],
    aspect_ratio: Annotated[
        str, Field(description="Aspect ratio for the video, e.g., '16:9'", pattern=r"^\d+:\d+$")
    ] = "9:16",
    person_generation: Annotated[
        str, Field(description="Allow person generation: 'allow_adult' or 'dont_allow'")
    ] = "dont_allow",
) -> Output:
    """Generate a video using the Gemini API (background task)."""
    task_id = str(uuid.uuid4())
    asyncio.create_task(_background_generate_video(task_id, prompt, aspect_ratio, person_generation))
    return Output(
        success=True,
        message="Video generation started. Use the task_id to check status or retrieve the video later.",
        task_id=task_id,
    )

export = generate_video

'''
class Output(BaseModel):
    """Response from the video generation tool."""
    success: bool
    message: str
    # video_files: list[str] = []

async def generate_video(
    prompt: Annotated[
        str, Field(description="Text prompt describing the video to generate", min_length=5)
    ],
    aspect_ratio: Annotated[
        str, Field(description="Aspect ratio for the video, e.g., '16:9'", pattern=r"^\d+:\d+$")
    ] = "9:16",
    person_generation: Annotated[
        str, Field(description="Allow person generation: 'allow_adult' or 'dont_allow'")
    ] = "dont_allow",
) -> Output:
    """Generate a video using the Gemini API."""
    try:
        client = genai.Client(api_key="AIzaSyDhuxHNLowdrZbwZ-qBhnQ3m4tdZxf2MIs")
        operation = client.models.generate_videos(
            model="veo-2.0-generate-001",
            prompt=prompt,
            config=types.GenerateVideosConfig(
                person_generation=person_generation,
                aspect_ratio=aspect_ratio,
            ),
        )

        # Poll until done (blocking, but GolfMCP will run this in an async context)
        while not operation.done:
            print("Waiting for video generation to complete, 10 more seconds...")
            await asyncio.sleep(10)
            operation = client.operations.get(operation)

        # video_files = []
        for idx, gen in enumerate(operation.response.generated_videos):
            filename = f"video_{idx}.mp4"
            client.files.download(file=gen.video)
            gen.video.save(filename)
            # video_files.append(filename)

        return Output(
            success=True,
            message="Video generation completed.",
            # video_files=video_files,
        )
    except Exception as e:
        return Output(
            success=False,
            message=f"Video generation failed: {str(e)}",
            # video_files=[],
        )

export = generate_video
'''