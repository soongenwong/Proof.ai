import asyncio
from generate import generate_video

async def main():
    result = await generate_video(
        prompt="A cat playing piano in a jazz bar, cinematic, 4K",
        aspect_ratio="16:9",
        person_generation="dont_allow"
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(main())