#!/usr/bin/env python3
"""
Voice-Controlled Video Generation System
ElevenLabs Conversational AI + Google Gemini Veo 2
"""

import os
import json
import asyncio
import requests
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ElevenLabs imports  
from elevenlabs.client import ElevenLabs

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY") 
ELEVENLABS_AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID")

if not all([GEMINI_API_KEY, ELEVENLABS_API_KEY]):
    raise ValueError("Missing required API keys in environment variables")

# Initialize clients
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
# genai.configure(api_key=GEMINI_API_KEY)

class VideoGeneratorGemini:
    """Handles Google Gemini (Veo 2) video generation"""

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.output_dir = Path("generated_videos")
        self.output_dir.mkdir(exist_ok=True)

    def generate_video(self, prompt: str, aspect_ratio: str = "16:9", person_generation: str = "dont_allow", **kwargs) -> Dict[str, Any]:
        """
        Generate video using Google Gemini (Veo 2) API.
        
        Args:
            prompt: Text description for video generation
            aspect_ratio: "16:9" (landscape) or "9:16" (portrait)
            person_generation: "dont_allow" or "allow_adult"
            **kwargs: Additional parameters (for compatibility)
        """
        try:
            logger.info(f"Generating video with Gemini Veo 2:")
            logger.info(f"  Prompt: '{prompt}'")
            logger.info(f"  Aspect ratio: {aspect_ratio}")
            logger.info(f"  Person generation: {person_generation}")
            
            # Start video generation
            operation = self.client.models.generate_videos(
                model="veo-2.0-generate-001",
                prompt=prompt,
                config=types.GenerateVideosConfig(
                    person_generation=person_generation,
                    aspect_ratio=aspect_ratio,
                ),
            )

            logger.info(f"Video generation started. Operation ID: {operation.name}")
            
            # Poll until done
            poll_count = 0
            max_polls = 30  # Max ~10 minutes (30 * 20 seconds)
            
            while not operation.done and poll_count < max_polls:
                poll_count += 1
                logger.info(f"Waiting for video generation... (attempt {poll_count}/{max_polls})")
                time.sleep(20)  # Wait 20 seconds between polls
                operation = self.client.operations.get(operation.name)

            if not operation.done:
                logger.error("Video generation timed out after 10 minutes")
                return {
                    "success": False,
                    "error": "Video generation timed out after 10 minutes",
                    "prompt": prompt,
                    "timestamp": datetime.now().isoformat()
                }

            # Check for errors
            if operation.error:
                logger.error(f"Video generation failed: {operation.error}")
                return {
                    "success": False,
                    "error": str(operation.error),
                    "prompt": prompt,
                    "timestamp": datetime.now().isoformat()
                }

            # Download generated videos
            output_paths = []
            video_urls = []
            
            for n, generated_video in enumerate(operation.response.generated_videos):
                # Create filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"gemini_video_{timestamp}_{n}.mp4"
                filepath = self.output_dir / filename
                
                try:
                    # Download video file
                    logger.info(f"Downloading video {n+1}...")
                    video_data = self.client.files.download(file=generated_video.video)
                    
                    # Save to local file
                    with open(filepath, 'wb') as f:
                        f.write(video_data)
                    
                    output_paths.append(str(filepath))
                    # For web access, you'd typically upload to cloud storage and return URL
                    # For now, return local file path
                    video_urls.append(f"file://{filepath.absolute()}")
                    
                    logger.info(f"Video saved to: {filepath}")
                    
                except Exception as e:
                    logger.error(f"Error downloading video {n}: {e}")
                    continue

            if not output_paths:
                return {
                    "success": False,
                    "error": "Failed to download any generated videos",
                    "prompt": prompt,
                    "timestamp": datetime.now().isoformat()
                }

            return {
                "success": True,
                "video_urls": video_urls,
                "local_paths": output_paths,
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "person_generation": person_generation,
                "generation_time_minutes": (poll_count * 20) / 60,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error generating video with Gemini: {e}")
            return {
                "success": False,
                "error": str(e),
                "prompt": prompt,
                "timestamp": datetime.now().isoformat()
            }

# Initialize video generator
video_gen_gemini = VideoGeneratorGemini()

# Tool Functions - These are called by the webhook handler

def generate_video_basic_tool(prompt: str) -> str:
    """Generate a video from a text prompt using default settings."""
    result = video_gen_gemini.generate_video(prompt)
    return json.dumps(result, indent=2)

def generate_video_advanced_tool(
    prompt: str, 
    style: str = "cinematic", 
    format_type: str = "landscape", 
    allow_people: str = "no"
) -> str:
    """Generate a video with advanced settings based on style preferences."""
    
    # Map format to aspect ratio
    aspect_ratio_map = {
        "landscape": "16:9",
        "portrait": "9:16",
        "vertical": "9:16",
        "horizontal": "16:9",
        "wide": "16:9",
        "mobile": "9:16"
    }
    
    # Map people setting
    person_generation_map = {
        "no": "dont_allow",
        "false": "dont_allow", 
        "yes": "allow_adult",
        "true": "allow_adult",
        "allow": "allow_adult",
        "adults": "allow_adult"
    }
    
    # Enhance prompt based on style
    style_prompts = {
        "cinematic": f"Cinematic shot of {prompt}, professional lighting, film grain, shallow depth of field, dramatic composition",
        "documentary": f"Documentary style footage of {prompt}, natural lighting, realistic, observational camera work",
        "artistic": f"Artistic interpretation of {prompt}, creative angles, dramatic composition, artistic lighting",
        "commercial": f"Commercial quality video of {prompt}, clean, professional, branded, high production value",
        "realistic": f"Realistic video of {prompt}, natural lighting, authentic, true-to-life",
        "dramatic": f"Dramatic scene of {prompt}, intense lighting, emotional, high contrast",
        "minimalist": f"Minimalist video of {prompt}, clean composition, simple, elegant",
        "vibrant": f"Vibrant and colorful video of {prompt}, rich colors, dynamic, energetic"
    }
    
    enhanced_prompt = style_prompts.get(style.lower(), prompt)
    aspect_ratio = aspect_ratio_map.get(format_type.lower(), "16:9")
    person_generation = person_generation_map.get(allow_people.lower(), "dont_allow")
    
    logger.info(f"Advanced generation: style={style}, format={format_type}, people={allow_people}")
    logger.info(f"Mapped to: aspect_ratio={aspect_ratio}, person_generation={person_generation}")
    
    result = video_gen_gemini.generate_video(
        prompt=enhanced_prompt,
        aspect_ratio=aspect_ratio,
        person_generation=person_generation
    )
    return json.dumps(result, indent=2)

def get_video_status_tool(video_path: str) -> str:
    """Check the status of a generated video file."""
    try:
        if video_path.startswith("file://"):
            file_path = video_path.replace("file://", "")
        else:
            file_path = video_path
            
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            status = {
                "video_path": video_path,
                "status": "available",
                "file_size_mb": round(file_size / (1024 * 1024), 2),
                "exists": True,
                "timestamp": datetime.now().isoformat()
            }
        else:
            status = {
                "video_path": video_path,
                "status": "not_found",
                "exists": False,
                "timestamp": datetime.now().isoformat()
            }
        return json.dumps(status, indent=2)
    except Exception as e:
        return json.dumps({
            "video_path": video_path,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }, indent=2)

def list_recent_videos_tool() -> str:
    """List recently generated videos from the output directory."""
    try:
        output_dir = Path("generated_videos")
        if not output_dir.exists():
            return json.dumps({
                "videos": [],
                "count": 0,
                "message": "No videos generated yet",
                "timestamp": datetime.now().isoformat()
            }, indent=2)
        
        video_files = list(output_dir.glob("*.mp4"))
        video_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)  # Sort by modification time
        
        videos = []
        for video_file in video_files[:10]:  # Last 10 videos
            stat = video_file.stat()
            videos.append({
                "filename": video_file.name,
                "path": str(video_file.absolute()),
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "url": f"file://{video_file.absolute()}"
            })
        
        return json.dumps({
            "videos": videos,
            "count": len(videos),
            "total_files": len(video_files),
            "output_directory": str(output_dir.absolute()),
            "timestamp": datetime.now().isoformat()
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }, indent=2)

class VoiceVideoAgent:
    """Main orchestrator for voice-controlled video generation"""
    
    def __init__(self):
        self.agent_id = ELEVENLABS_AGENT_ID
        
    def create_agent_config(self) -> Dict[str, Any]:
        """Create ElevenLabs agent configuration"""
        
        system_prompt = """You are a professional video creation assistant powered by Google Gemini Veo 2. 
        
Your role is to help users create high-quality AI-generated videos from text descriptions. You have access to advanced video generation tools and can:

1. Generate videos from simple text prompts using Gemini Veo 2
2. Create videos with specific styles (cinematic, documentary, artistic, commercial, realistic, dramatic)
3. Control video format (landscape 16:9 or portrait 9:16)
4. Handle person generation settings (allow adults or don't allow people)
5. Check video status and provide updates
6. List recent video creations

When users request videos:
- Ask clarifying questions about style, mood, and format requirements
- Suggest improvements to prompts for better results
- Explain that video generation takes 2-10 minutes with Gemini Veo 2
- Offer format options: landscape (16:9) for desktop/TV or portrait (9:16) for mobile/social media
- Ask about including people in videos (some use cases may require this setting)

Available tools:
- generate_video_basic: For simple video generation with default settings
- generate_video_advanced: For videos with specific style, format, and people settings
- get_video_status: To check if a video file exists and get its details
- list_recent_videos: To show recent video creations

Video generation capabilities:
- High-quality video output using Google's Veo 2 model
- Support for 16:9 (landscape) and 9:16 (portrait) aspect ratios
- Option to include or exclude people in videos
- Various style enhancements for different use cases

Always be helpful, creative, and provide clear explanations of what you're doing. Remind users that Gemini Veo 2 produces very high-quality results but takes several minutes to generate."""

        # Define tools that the agent can call
        tools = [
            {
                "name": "generate_video_basic",
                "description": "Generate a video from a text prompt using default settings (16:9, no people)",
                "webhook_url": "http://localhost:8000/tools/generate_video_basic"
            },
            {
                "name": "generate_video_advanced", 
                "description": "Generate a video with specific style, format (landscape/portrait), and people settings",
                "webhook_url": "http://localhost:8000/tools/generate_video_advanced"
            },
            {
                "name": "get_video_status",
                "description": "Check the status and details of a generated video file",
                "webhook_url": "http://localhost:8000/tools/get_video_status"
            },
            {
                "name": "list_recent_videos",
                "description": "List recently generated videos with details",
                "webhook_url": "http://localhost:8000/tools/list_recent_videos"
            }
        ]
        
        return {
            "name": "Gemini Veo 2 Video Creation Assistant",
            "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel voice
            "system_prompt": system_prompt,
            "tools": tools,
            "language": "en",
            "max_conversation_length": 30  # seconds
        }

async def create_agent():
    """Create and configure the ElevenLabs conversational agent"""
    try:
        # Create agent configuration
        agent = VoiceVideoAgent()
        config = agent.create_agent_config()
        
        # Create the agent via ElevenLabs API
        response = elevenlabs_client.conversational_ai.create_agent(
            name=config["name"],
            voice_id=config["voice_id"],
            system_prompt=config["system_prompt"],
            tools=config["tools"]
        )
        
        agent_id = response.agent_id
        logger.info(f"Created ElevenLabs agent with ID: {agent_id}")
        logger.info("Add this to your .env file as ELEVENLABS_AGENT_ID")
        
        return agent_id
        
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        return None

async def start_webhook_server():
    """Start webhook server to handle tool calls from ElevenLabs agent"""
    from fastapi import FastAPI, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    import uvicorn
    
    app = FastAPI(title="Gemini Veo 2 Video Generation Server")

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Serve generated videos as static files
    if Path("generated_videos").exists():
        app.mount("/videos", StaticFiles(directory="generated_videos"), name="videos")
    
    @app.post("/tools/{tool_name}")
    async def handle_tool_call(tool_name: str, request: Request):
        """Handle tool calls from ElevenLabs agent"""
        try:
            data = await request.json()
            parameters = data.get("parameters", {})
            
            logger.info(f"Handling tool call: {tool_name}")
            logger.info(f"Parameters: {parameters}")
            
            if tool_name == "generate_video_basic":
                prompt = parameters.get("prompt", "")
                if not prompt:
                    result_json = json.dumps({"error": "No prompt provided"}, indent=2)
                else:
                    result = video_gen_gemini.generate_video(prompt)
                    result_json = json.dumps(result, indent=2)
                
            elif tool_name == "generate_video_advanced":
                prompt = parameters.get("prompt", "")
                style = parameters.get("style", "cinematic")
                format_type = parameters.get("format_type", "landscape")
                allow_people = parameters.get("allow_people", "no")
                
                if not prompt:
                    result_json = json.dumps({"error": "No prompt provided"}, indent=2)
                else:
                    result_json = generate_video_advanced_tool(prompt, style, format_type, allow_people)
                
            elif tool_name == "get_video_status":
                video_path = parameters.get("video_path", "")
                result_json = get_video_status_tool(video_path)
                    
            elif tool_name == "list_recent_videos":
                result_json = list_recent_videos_tool()
                
            else:
                result_json = json.dumps({"error": f"Unknown tool: {tool_name}"}, indent=2)
                
            logger.info(f"Tool call completed: {tool_name}")
            return {"result": result_json}
            
        except Exception as e:
            logger.error(f"Error handling tool call {tool_name}: {e}")
            return {"error": str(e)}
    
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy", 
            "service": "Gemini Veo 2 Video Generator",
            "timestamp": datetime.now().isoformat()
        }
    
    @app.get("/")
    async def root():
        return {
            "message": "Gemini Veo 2 Video Generation API",
            "status": "running",
            "endpoints": {
                "health": "/health",
                "tools": "/tools/{tool_name}",
                "videos": "/videos/ (static file serving)"
            }
        }
    
    # Start server
    logger.info("Starting Gemini Veo 2 webhook server on http://localhost:8000")
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    """Main application entry point"""
    logger.info("🎬 Starting Gemini Veo 2 Voice-Controlled Video Generation System")
    logger.info("=" * 60)
    
    # Check API keys
    if not GEMINI_API_KEY:
        logger.error("❌ GEMINI_API_KEY not found in environment variables")
        return
        
    if not ELEVENLABS_API_KEY:
        logger.error("❌ ELEVENLABS_API_KEY not found in environment variables") 
        return
    
    # Check if agent ID exists
    if not ELEVENLABS_AGENT_ID:
        logger.info("No agent ID found. Creating new ElevenLabs agent...")
        agent_id = await create_agent()
        if agent_id:
            logger.info(f"✅ Agent created! Add this to your .env file:")
            logger.info(f"ELEVENLABS_AGENT_ID={agent_id}")
            return
        else:
            logger.error("❌ Failed to create agent")
            return
    
    # Start the webhook server
    try:
        logger.info("🚀 Starting webhook server...")
        logger.info("Ready to generate videos with Gemini Veo 2!")
        await start_webhook_server()
        
    except KeyboardInterrupt:
        logger.info("👋 Shutting down...")
    except Exception as e:
        logger.error(f"❌ Error running application: {e}")

if __name__ == "__main__":
    asyncio.run(main())