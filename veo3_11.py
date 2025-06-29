#!/usr/bin/env python3
"""
Voice-Controlled Video Generation System
ElevenLabs Conversational AI + Google Gemini Veo 3
Updated and Complete Implementation
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
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY") 
ELEVENLABS_AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID")

if not all([GEMINI_API_KEY, ELEVENLABS_API_KEY]):
    raise ValueError("Missing required API keys in environment variables")

# Initialize clients
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

class VideoGeneratorVeo3:
    """Handles Google Gemini Veo 3 video generation"""

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.output_dir = Path("generated_videos")
        self.output_dir.mkdir(exist_ok=True)
        
        # Veo 3 model identifier - CONFIRMED WORKING as of June 2025
        self.model_name = "veo-2.0-generate-001"  #"veo-3.0-generate-preview"  # Official Veo 3 model name

        logger.info(f"Initialized Veo 3 Video Generator with model: {self.model_name}")

    def generate_video_variations(self, prompt: str, n_variations: int = 2, aspect_ratio: str = "16:9", person_generation: str = "dont_allow") -> Dict[str, Any]:
        """
        Generate multiple variations of a single video concept using Veo 3.
        
        Args:
            prompt: Text description for video generation
            n_variations: Number of video variations to generate (default 2)
            aspect_ratio: "16:9" (landscape) or "9:16" (portrait)
            person_generation: "dont_allow" or "allow_adult"
        """
        try:
            logger.info(f"🎬 Generating {n_variations} variations with Gemini Veo 3:")
            logger.info(f"  Prompt: '{prompt}'")
            logger.info(f"  Aspect ratio: {aspect_ratio}")
            logger.info(f"  Person generation: {person_generation}")
            
            all_videos = []
            
            for i in range(n_variations):
                logger.info(f"\n🎬 Generating variation {i+1}/{n_variations}")
                
                try:
                    # Start video generation with Veo 3 (includes native audio)
                    operation = self.client.models.generate_videos(
                        model=self.model_name,
                        prompt=prompt,
                        config=types.GenerateVideosConfig(
                            person_generation=person_generation,
                            aspect_ratio=aspect_ratio,
                            # Generate 1 video per API call for better error handling
                            # (Your loop-based approach is superior to batch generation)
                        ),
                    )

                    logger.info(f"Video generation started. Operation ID: {operation.name}")
                    
                    # Poll until done with increased timeout for Veo 3
                    poll_count = 0
                    max_polls = 60  # Max ~20 minutes (60 * 20 seconds) for Veo 3
                    
                    while not operation.done and poll_count < max_polls:
                        poll_count += 1
                        logger.info(f"⏳ Waiting for generation... (attempt {poll_count}/{max_polls})")
                        time.sleep(20)  # Wait 20 seconds between polls
                        operation = self.client.operations.get(operation)

                    if not operation.done:
                        logger.error(f"❌ Variation {i+1} timed out after 20 minutes")
                        continue

                    # Check for errors
                    if hasattr(operation, 'error') and operation.error:
                        logger.error(f"❌ Variation {i+1} failed: {operation.error}")
                        continue

                    # Save generated videos
                    if operation.response and hasattr(operation.response, 'generated_videos') and operation.response.generated_videos:
                        for vid_idx, generated_video in enumerate(operation.response.generated_videos):
                            try:
                                # Download video file
                                video_data = self.client.files.download(file=generated_video.video)
                                
                                # Create filename
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                filename = f"veo3_variation_{i+1}_video_{vid_idx+1}_{timestamp}.mp4"
                                filepath = self.output_dir / filename
                                
                                # Save video file
                                with open(filepath, 'wb') as f:
                                    f.write(video_data)
                                
                                all_videos.append({
                                    "variation": i+1,
                                    "video_index": vid_idx+1,
                                    "filename": filename,
                                    "local_path": str(filepath),
                                    "url": f"http://localhost:8000/videos/{filename}",
                                    "size_mb": round(len(video_data) / (1024 * 1024), 2)
                                })
                                
                                logger.info(f"✅ Saved variation {i+1}, video {vid_idx+1}: {filename}")
                                
                            except Exception as e:
                                logger.error(f"❌ Error saving variation {i+1}, video {vid_idx}: {e}")
                                continue
                    else:
                        logger.error(f"❌ No videos generated for variation {i+1}")
                        
                except Exception as e:
                    logger.error(f"❌ Error generating variation {i+1}: {e}")
                    continue

            if not all_videos:
                return {
                    "success": False,
                    "error": "Failed to generate any video variations",
                    "prompt": prompt,
                    "timestamp": datetime.now().isoformat()
                }

            return {
                "success": True,
                "total_videos": len(all_videos),
                "variations_requested": n_variations,
                "videos": all_videos,
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "person_generation": person_generation,
                "model": self.model_name,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error generating video variations: {e}")
            return {
                "success": False,
                "error": str(e),
                "prompt": prompt,
                "timestamp": datetime.now().isoformat()
            }

    def generate_video(self, prompt: str, aspect_ratio: str = "16:9", person_generation: str = "dont_allow", **kwargs) -> Dict[str, Any]:
        """
        Generate single video using Google Gemini Veo 3 API.
        For compatibility with existing code.
        """
        result = self.generate_video_variations(prompt, n_variations=1, aspect_ratio=aspect_ratio, person_generation=person_generation)
        
        if result["success"] and result["videos"]:
            video = result["videos"][0]
            return {
                "success": True,
                "video_urls": [video["url"]],
                "local_paths": [video["local_path"]],
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "person_generation": person_generation,
                "model": self.model_name,
                "timestamp": result["timestamp"]
            }
        else:
            return result

# Initialize video generator
video_gen_veo3 = VideoGeneratorVeo3()

# Enhanced Tool Functions

def generate_video_basic_tool(prompt: str) -> str:
    """Generate 2 video variations from a text prompt using Veo 3 default settings."""
    result = video_gen_veo3.generate_video_variations(prompt, n_variations=2)
    return json.dumps(result, indent=2)

def generate_video_single_tool(prompt: str) -> str:
    """Generate a single video from a text prompt using Veo 3."""
    result = video_gen_veo3.generate_video(prompt)
    return json.dumps(result, indent=2)

def generate_video_advanced_tool(
    prompt: str, 
    style: str = "cinematic", 
    format_type: str = "landscape", 
    allow_people: str = "no",
    variations: str = "2"
) -> str:
    """Generate videos with advanced settings using Veo 3."""
    
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
    
    # Parse variations count
    try:
        n_variations = int(variations)
        n_variations = max(1, min(n_variations, 5))  # Limit to 1-5 variations
    except:
        n_variations = 2  # Default to 2
    
    # Enhanced style prompts for Veo 3
    style_prompts = {
        "cinematic": f"Cinematic masterpiece of {prompt}, professional cinematography, film grain, shallow depth of field, dramatic composition, movie-quality lighting",
        "documentary": f"Documentary style footage of {prompt}, natural lighting, realistic, observational camera work, authentic feel",
        "artistic": f"Artistic interpretation of {prompt}, creative angles, dramatic composition, artistic lighting, visual storytelling",
        "commercial": f"Commercial quality video of {prompt}, clean, professional, branded, high production value, polished",
        "realistic": f"Photorealistic video of {prompt}, natural lighting, authentic, true-to-life, high detail",
        "dramatic": f"Dramatic scene of {prompt}, intense lighting, emotional, high contrast, powerful visuals",
        "minimalist": f"Minimalist video of {prompt}, clean composition, simple, elegant, focused",
        "vibrant": f"Vibrant and colorful video of {prompt}, rich colors, dynamic, energetic, visually striking"
    }
    
    enhanced_prompt = style_prompts.get(style.lower(), prompt)
    aspect_ratio = aspect_ratio_map.get(format_type.lower(), "16:9")
    person_generation = person_generation_map.get(allow_people.lower(), "dont_allow")
    
    logger.info(f"Advanced Veo 3 generation: style={style}, format={format_type}, people={allow_people}, variations={n_variations}")
    logger.info(f"Mapped to: aspect_ratio={aspect_ratio}, person_generation={person_generation}")
    
    result = video_gen_veo3.generate_video_variations(
        prompt=enhanced_prompt,
        n_variations=n_variations,
        aspect_ratio=aspect_ratio,
        person_generation=person_generation
    )
    return json.dumps(result, indent=2)

def extract_video_prompt_from_speech(text: str) -> str:
    """
    Extract and enhance video prompt from speech input.
    Enhanced for better speech-to-video conversion.
    """
    # Basic cleaning and enhancement
    text = text.strip()
    
    # Remove common speech artifacts and filler words
    speech_artifacts = ["um", "uh", "like", "you know", "so", "well", "actually", "basically"]
    words = text.split()
    cleaned_words = [word for word in words if word.lower() not in speech_artifacts]
    cleaned_text = " ".join(cleaned_words)
    
    # Enhanced prompt engineering for Veo 3
    if len(cleaned_text) < 15:
        # Very short prompts - add substantial enhancement
        enhanced_prompt = f"High-quality cinematic video of {cleaned_text}, professional lighting, detailed visuals, smooth camera movement"
    elif len(cleaned_text) < 30:
        # Short prompts - add moderate enhancement
        enhanced_prompt = f"Cinematic shot of {cleaned_text}, professional quality, detailed"
    else:
        # Longer prompts - minimal enhancement
        enhanced_prompt = cleaned_text
    
    logger.info(f"Speech to Veo 3 prompt: '{text}' -> '{enhanced_prompt}'")
    return enhanced_prompt

def generate_from_speech_tool(speech_text: str, style: str = "cinematic", format_type: str = "landscape") -> str:
    """Generate 2 video variations from speech input using Veo 3."""
    
    # Extract and enhance the prompt from speech
    prompt = extract_video_prompt_from_speech(speech_text)
    
    # Generate 2 variations by default for Veo 3
    return generate_video_advanced_tool(
        prompt=prompt,
        style=style,
        format_type=format_type,
        allow_people="no",
        variations="2"
    )

def get_video_status_tool(video_path: str) -> str:
    """Check the status of a generated video file."""
    try:
        if video_path.startswith("file://"):
            file_path = video_path.replace("file://", "")
        elif video_path.startswith("http://localhost:8000/videos/"):
            filename = video_path.split("/")[-1]
            file_path = str(Path("generated_videos") / filename)
        else:
            file_path = video_path
            
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            status = {
                "video_path": video_path,
                "status": "available",
                "file_size_mb": round(file_size / (1024 * 1024), 2),
                "exists": True,
                "model": "veo-3",
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
        video_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        videos = []
        for video_file in video_files[:10]:  # Last 10 videos
            stat = video_file.stat()
            videos.append({
                "filename": video_file.name,
                "path": str(video_file.absolute()),
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "url": f"http://localhost:8000/videos/{video_file.name}",
                "model": "veo-3" if "veo3" in video_file.name else "unknown"
            })
        
        return json.dumps({
            "videos": videos,
            "count": len(videos),
            "total_files": len(video_files),
            "output_directory": str(output_dir.absolute()),
            "model": "veo-3",
            "timestamp": datetime.now().isoformat()
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }, indent=2)

class VoiceVideoAgent:
    """Main orchestrator for voice-controlled video generation with Veo 3"""
    
    def __init__(self):
        self.agent_id = ELEVENLABS_AGENT_ID
        
    def create_agent_config(self) -> Dict[str, Any]:
        """Create ElevenLabs agent configuration for Veo 3"""
        
        system_prompt = """You are a professional video creation assistant powered by Google Gemini Veo 3, the latest and most advanced AI video generation model.

Your specialty is creating high-quality AI-generated videos from voice input. By default, you generate 2 video variations for each request to give users creative options.

When users speak to you about creating videos:
1. Listen carefully to extract the core visual concept from their speech
2. Ask clarifying questions about style, mood, and format if needed
3. Generate 2 video variations by default (users love having options!)
4. Explain that Veo 3 creates exceptional quality videos but may take 3-15 minutes per generation

Key Features of Veo 3:
- Superior video quality and realism
- Better understanding of complex prompts
- Enhanced motion and physics
- Improved consistency across frames

Available tools:
- generate_video_basic: Creates 2 video variations with default settings (most common)
- generate_video_single: Creates just 1 video if specifically requested
- generate_video_advanced: Creates videos with specific style, format, people settings, and custom variation count
- generate_from_speech: Optimized for processing natural speech input into video prompts
- get_video_status: Check video file status
- list_recent_videos: Show recent creations

Default behavior: Generate 2 variations in 16:9 landscape format, cinematic style, no people allowed.

Be conversational, creative, and help users refine their video ideas. Suggest improvements and explain the Veo 3 generation process. Always mention you're using the cutting-edge Veo 3 model for superior results."""

        # Define tools that the agent can call
        tools = [
            {
                "name": "generate_video_basic",
                "description": "Generate 2 video variations from a text prompt using Veo 3 default settings (16:9, no people, cinematic style)",
                "webhook_url": "http://localhost:8000/tools/generate_video_basic"
            },
            {
                "name": "generate_video_single", 
                "description": "Generate just 1 video from a text prompt using Veo 3 (when user specifically wants only one)",
                "webhook_url": "http://localhost:8000/tools/generate_video_single"
            },
            {
                "name": "generate_video_advanced", 
                "description": "Generate videos with specific style, format (landscape/portrait), people settings, and variation count using Veo 3",
                "webhook_url": "http://localhost:8000/tools/generate_video_advanced"
            },
            {
                "name": "generate_from_speech",
                "description": "Process natural speech input into enhanced video prompts and generate 2 variations using Veo 3",
                "webhook_url": "http://localhost:8000/tools/generate_from_speech"
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
            "name": "Gemini Veo 3 Voice Video Assistant",
            "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel voice (you can change this)
            "system_prompt": system_prompt,
            "tools": tools,
            "language": "en",
            "max_conversation_length": 45  # seconds - increased for complex video requests
        }

async def create_agent():
    """Create and configure the ElevenLabs conversational agent"""
    try:
        agent = VoiceVideoAgent()
        config = agent.create_agent_config()
        
        response = elevenlabs_client.conversational_ai.create_agent(
            name=config["name"],
            voice_id=config["voice_id"],
            system_prompt=config["system_prompt"],
            tools=config["tools"]
        )
        
        agent_id = response.agent_id
        logger.info(f"✅ Created ElevenLabs agent with ID: {agent_id}")
        logger.info("Add this to your .env file as ELEVENLABS_AGENT_ID")
        
        return agent_id
        
    except Exception as e:
        logger.error(f"❌ Error creating agent: {e}")
        return None

async def start_webhook_server():
    """Start webhook server to handle tool calls from ElevenLabs agent"""
    from fastapi import FastAPI, Request, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import JSONResponse
    import uvicorn
    
    app = FastAPI(title="Gemini Veo 3 Voice Video Generation Server")

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
    else:
        Path("generated_videos").mkdir(exist_ok=True)
        app.mount("/videos", StaticFiles(directory="generated_videos"), name="videos")
    
    @app.post("/tools/{tool_name}")
    async def handle_tool_call(tool_name: str, request: Request):
        """Handle tool calls from ElevenLabs agent"""
        try:
            data = await request.json()
            parameters = data.get("parameters", {})
            
            logger.info(f"🔧 Handling tool call: {tool_name}")
            logger.info(f"📝 Parameters: {parameters}")
            
            if tool_name == "generate_video_basic":
                prompt = parameters.get("prompt", "")
                if not prompt:
                    result_json = json.dumps({"error": "No prompt provided"}, indent=2)
                else:
                    result_json = generate_video_basic_tool(prompt)
                
            elif tool_name == "generate_video_single":
                prompt = parameters.get("prompt", "")
                if not prompt:
                    result_json = json.dumps({"error": "No prompt provided"}, indent=2)
                else:
                    result_json = generate_video_single_tool(prompt)
                
            elif tool_name == "generate_video_advanced":
                prompt = parameters.get("prompt", "")
                style = parameters.get("style", "cinematic")
                format_type = parameters.get("format_type", "landscape")
                allow_people = parameters.get("allow_people", "no")
                variations = parameters.get("variations", "2")
                
                if not prompt:
                    result_json = json.dumps({"error": "No prompt provided"}, indent=2)
                else:
                    result_json = generate_video_advanced_tool(prompt, style, format_type, allow_people, variations)
                
            elif tool_name == "generate_from_speech":
                speech_text = parameters.get("speech_text", "")
                style = parameters.get("style", "cinematic")
                format_type = parameters.get("format_type", "landscape")
                
                if not speech_text:
                    result_json = json.dumps({"error": "No speech text provided"}, indent=2)
                else:
                    result_json = generate_from_speech_tool(speech_text, style, format_type)
                
            elif tool_name == "get_video_status":
                video_path = parameters.get("video_path", "")
                result_json = get_video_status_tool(video_path)
                    
            elif tool_name == "list_recent_videos":
                result_json = list_recent_videos_tool()
                
            else:
                result_json = json.dumps({"error": f"Unknown tool: {tool_name}"}, indent=2)
                
            logger.info(f"✅ Tool call completed: {tool_name}")
            return {"result": result_json}
            
        except Exception as e:
            logger.error(f"❌ Error handling tool call {tool_name}: {e}")
            return {"error": str(e)}
    
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy", 
            "service": "Gemini Veo 3 Voice Video Generator",
            "model": "veo-3.0-generate-001",
            "timestamp": datetime.now().isoformat()
        }
    
    @app.get("/")
    async def root():
        return {
            "message": "Gemini Veo 3 Voice Video Generation API",
            "status": "running",
            "model": "veo-3.0-generate-001",
            "default_behavior": "Generate 2 video variations per request",
            "features": ["Voice input", "Multiple variations", "Advanced styling"],
            "endpoints": {
                "health": "/health",
                "tools": "/tools/{tool_name}",
                "videos": "/videos/ (static file serving)"
            }
        }
    
    # Start server
    logger.info("🚀 Starting Gemini Veo 3 webhook server on http://localhost:8000")
    logger.info("🎬 Default: Generate 2 video variations per request")
    logger.info("🎤 Ready for voice input!")
    
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    """Main application entry point"""
    logger.info("🎬 Starting Gemini Veo 3 Voice-Controlled Video Generation System")
    logger.info("🚀 Enhanced with Veo 3 - Next Generation AI Video")
    logger.info("🎯 Default: 2 video variations per request")
    logger.info("=" * 70)
    
    # Check API keys
    if not GEMINI_API_KEY:
        logger.error("❌ GEMINI_API_KEY not found in environment variables")
        logger.info("Get your API key from: https://aistudio.google.com/")
        return
        
    if not ELEVENLABS_API_KEY:
        logger.error("❌ ELEVENLABS_API_KEY not found in environment variables") 
        logger.info("Get your API key from: https://elevenlabs.io/")
        return
    
    # Handle agent creation/verification
    if not ELEVENLABS_AGENT_ID:
        logger.info("🤖 No agent ID found. Creating new ElevenLabs agent...")
        agent_id = await create_agent()
        if agent_id:
            logger.info(f"✅ Agent created successfully!")
            logger.info(f"📝 Add this to your .env file:")
            logger.info(f"ELEVENLABS_AGENT_ID={agent_id}")
            logger.info("")
            logger.info("🔄 Please restart the application after adding the agent ID to .env")
            return
        else:
            logger.error("❌ Failed to create agent")
            return
    else:
        logger.info(f"🤖 Using existing agent ID: {ELEVENLABS_AGENT_ID}")
    
    # Start the webhook server
    try:
        logger.info("🚀 Starting webhook server...")
        logger.info("🎤 Ready to generate videos with Gemini Veo 3!")
        logger.info("💬 Speak to your ElevenLabs agent to generate videos")
        await start_webhook_server()
        
    except KeyboardInterrupt:
        logger.info("👋 Shutting down gracefully...")
    except Exception as e:
        logger.error(f"❌ Error running application: {e}")

if __name__ == "__main__":
    asyncio.run(main())