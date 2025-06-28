#!/usr/bin/env python3
"""
Voice-Controlled Video Generation System
ElevenLabs Conversational AI + Stability AI
"""

import os
import json
import asyncio
import requests
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# ElevenLabs imports  
from elevenlabs.client import ElevenLabs

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global configuration
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY") 
ELEVENLABS_AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID")

if not all([STABILITY_API_KEY, ELEVENLABS_API_KEY]):
    raise ValueError("Missing required API keys in environment variables")

# Initialize ElevenLabs client
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

class VideoGenerator:
    """Handles Stability AI video generation"""
    
    def __init__(self):
        self.api_key = STABILITY_API_KEY
        self.base_url = "https://api.stability.ai/v2beta/image-to-video"
        
    def generate_video(self, prompt: str, image_path: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Generate video using Stability AI API (image-to-video).
        If image_path is provided, uploads the image as part of the request.
        """
        url = f"{self.base_url}"
        headers = {
            "authorization": f"Bearer {self.api_key}"
        }

        files = {}
        if image_path:
            try:
                files["image"] = open(image_path, "rb")
            except Exception as e:
                logger.error(f"Error opening image file: {e}")
                return {
                    "success": False,
                    "error": f"Error opening image file: {e}",
                    "prompt": prompt,
                    "timestamp": datetime.now().isoformat()
                }

        # Use data for non-file parameters
        data = {
            "seed": kwargs.get("seed", 0),
            "cfg_scale": kwargs.get("cfg_scale", 1.8),
            "motion_bucket_id": kwargs.get("motion_bucket_id", 127),
            # You can add more parameters as needed
        }

        try:
            logger.info(f"Generating video with prompt: {prompt} and image: {image_path}")
            response = requests.post(url, headers=headers, files=files if files else None, data=data, timeout=300)

            if files:
                files["image"].close()

            response.raise_for_status()
            result = response.json()
            generation_id = result.get('id')

            logger.info(f"Video generation started. Generation ID: {generation_id}")
            return {
                "success": True,
                "generation_id": generation_id,
                "prompt": prompt,
                "parameters": data,
                "timestamp": datetime.now().isoformat()
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error generating video: {e}")
            return {
                "success": False,
                "error": str(e),
                "prompt": prompt,
                "timestamp": datetime.now().isoformat()
            }

# Initialize video generator
video_gen = VideoGenerator()

# Tool Functions - These are called by the webhook handler

def generate_video_basic_tool(prompt: str) -> str:
    """Generate a video from a text prompt using default settings."""
    result = video_gen.generate_video(prompt)
    return json.dumps(result, indent=2)

def generate_video_advanced_tool(prompt: str, style: str = "cinematic", duration: str = "short", quality: str = "high") -> str:
    """Generate a video with advanced settings based on style preferences."""
    
    # Map style to parameters
    style_params = {
        "cinematic": {"cfg_scale": 9, "steps": 60, "motion_bucket_id": 180},
        "documentary": {"cfg_scale": 7, "steps": 50, "motion_bucket_id": 127},
        "artistic": {"cfg_scale": 12, "steps": 70, "motion_bucket_id": 200},
        "commercial": {"cfg_scale": 8, "steps": 55, "motion_bucket_id": 150}
    }
    
    # Map duration to frame settings
    duration_params = {
        "short": {"frame_rate": 30},
        "medium": {"frame_rate": 24}, 
        "long": {"frame_rate": 20}
    }
    
    # Map quality to resolution
    quality_params = {
        "high": {"width": 1024, "height": 576, "steps": 60},
        "medium": {"width": 768, "height": 432, "steps": 50},
        "fast": {"width": 512, "height": 288, "steps": 30}
    }
    
    # Combine parameters
    params = {}
    params.update(style_params.get(style, style_params["cinematic"]))
    params.update(duration_params.get(duration, duration_params["medium"]))
    params.update(quality_params.get(quality, quality_params["high"]))
    
    # Enhance prompt based on style
    style_prompts = {
        "cinematic": f"Cinematic shot of {prompt}, professional lighting, film grain, shallow depth of field",
        "documentary": f"Documentary style footage of {prompt}, natural lighting, realistic",
        "artistic": f"Artistic interpretation of {prompt}, creative angles, dramatic composition",
        "commercial": f"Commercial quality video of {prompt}, clean, professional, branded"
    }
    
    enhanced_prompt = style_prompts.get(style, prompt)
    
    result = video_gen.generate_video(enhanced_prompt, **params)
    return json.dumps(result, indent=2)

class VoiceVideoAgent:
    """Main orchestrator for voice-controlled video generation"""
    
    def __init__(self):
        self.agent_id = ELEVENLABS_AGENT_ID
        
    def create_agent_config(self) -> Dict[str, Any]:
        """Create ElevenLabs agent configuration"""
        
        system_prompt = """You are a professional video creation assistant powered by Stability AI. 
        
Your role is to help users create high-quality videos from text descriptions. You have access to advanced video generation tools and can:

1. Generate videos from simple text prompts
2. Create videos with specific styles (cinematic, documentary, artistic, commercial)
3. Adjust quality and duration settings
4. Check video status and provide updates
5. List recent video creations

When users request videos:
- Ask clarifying questions about style, mood, and requirements
- Suggest improvements to prompts for better results
- Explain the video generation process
- Provide realistic timeframes (2-5 minutes for generation)

Available tools:
- generate_video_basic: For simple video generation
- generate_video_advanced: For videos with specific style requirements
- get_video_status: To check if a video is ready
- list_recent_videos: To show recent creations

Always be helpful, creative, and provide clear explanations of what you're doing."""

        # Define tools that the agent can call
        tools = [
            {
                "name": "generate_video_basic",
                "description": "Generate a video from a text prompt using default settings",
                "webhook_url": "http://localhost:8000/tools/generate_video_basic"
            },
            {
                "name": "generate_video_advanced", 
                "description": "Generate a video with specific style and quality settings",
                "webhook_url": "http://localhost:8000/tools/generate_video_advanced"
            },
            {
                "name": "get_video_status",
                "description": "Check the status and availability of a generated video",
                "webhook_url": "http://localhost:8000/tools/get_video_status"
            },
            {
                "name": "list_recent_videos",
                "description": "List recently generated videos",
                "webhook_url": "http://localhost:8000/tools/list_recent_videos"
            }
        ]
        
        return {
            "name": "Video Creation Assistant",
            "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel voice
            "system_prompt": system_prompt,
            "tools": tools,
            "language": "en",
            "max_conversation_length": 300  # seconds
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
    import uvicorn
    
    app = FastAPI(title="Video Generation Tool Server")
    
    @app.post("/tools/{tool_name}")
    async def handle_tool_call(tool_name: str, request: Request):
        """Handle tool calls from ElevenLabs agent"""
        try:
            data = await request.json()
            parameters = data.get("parameters", {})
            
            # Call the actual functions directly (not the FastMCP wrapped versions)
            if tool_name == "generate_video_basic":
                prompt = parameters.get("prompt", "")
                result = video_gen.generate_video(prompt)
                result_json = json.dumps(result, indent=2)
                
            elif tool_name == "generate_video_advanced":
                prompt = parameters.get("prompt", "")
                style = parameters.get("style", "cinematic")
                duration = parameters.get("duration", "short")
                quality = parameters.get("quality", "high")
                
                # Map style to parameters
                style_params = {
                    "cinematic": {"cfg_scale": 9, "steps": 60, "motion_bucket_id": 180},
                    "documentary": {"cfg_scale": 7, "steps": 50, "motion_bucket_id": 127},
                    "artistic": {"cfg_scale": 12, "steps": 70, "motion_bucket_id": 200},
                    "commercial": {"cfg_scale": 8, "steps": 55, "motion_bucket_id": 150}
                }
                
                # Map duration to frame settings
                duration_params = {
                    "short": {"frame_rate": 30},
                    "medium": {"frame_rate": 24}, 
                    "long": {"frame_rate": 20}
                }
                
                # Map quality to resolution
                quality_params = {
                    "high": {"width": 1024, "height": 576, "steps": 60},
                    "medium": {"width": 768, "height": 432, "steps": 50},
                    "fast": {"width": 512, "height": 288, "steps": 30}
                }
                
                # Combine parameters
                params = {}
                params.update(style_params.get(style, style_params["cinematic"]))
                params.update(duration_params.get(duration, duration_params["medium"]))
                params.update(quality_params.get(quality, quality_params["high"]))
                
                # Enhance prompt based on style
                style_prompts = {
                    "cinematic": f"Cinematic shot of {prompt}, professional lighting, film grain, shallow depth of field",
                    "documentary": f"Documentary style footage of {prompt}, natural lighting, realistic",
                    "artistic": f"Artistic interpretation of {prompt}, creative angles, dramatic composition",
                    "commercial": f"Commercial quality video of {prompt}, clean, professional, branded"
                }
                
                enhanced_prompt = style_prompts.get(style, prompt)
                result = video_gen.generate_video(enhanced_prompt, **params)
                result_json = json.dumps(result, indent=2)
                
            elif tool_name == "get_video_status":
                video_url = parameters.get("video_url", "")
                try:
                    response = requests.head(video_url, timeout=10)
                    status = {
                        "video_url": video_url,
                        "status": "available" if response.status_code == 200 else "unavailable",
                        "status_code": response.status_code,
                        "content_length": response.headers.get("content-length", "unknown"),
                        "timestamp": datetime.now().isoformat()
                    }
                    result_json = json.dumps(status, indent=2)
                except Exception as e:
                    result_json = json.dumps({
                        "video_url": video_url,
                        "status": "error",
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    }, indent=2)
                    
            elif tool_name == "list_recent_videos":
                recent_videos = {
                    "message": "Recent videos would be listed here",
                    "note": "In production, this would query a database of user's videos",
                    "timestamp": datetime.now().isoformat()
                }
                result_json = json.dumps(recent_videos, indent=2)
                
            else:
                result_json = json.dumps({"error": f"Unknown tool: {tool_name}"})
                
            return {"result": result_json}
            
        except Exception as e:
            logger.error(f"Error handling tool call {tool_name}: {e}")
            return {"error": str(e)}
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "timestamp": datetime.now().isoformat()}
    
    # Start server
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    """Main application entry point"""
    logger.info("Starting Voice-Controlled Video Generation System")
    
    # Check if agent ID exists
    if not ELEVENLABS_AGENT_ID:
        logger.info("No agent ID found. Creating new agent...")
        agent_id = await create_agent()
        if agent_id:
            logger.info(f"Agent created! Add ELEVENLABS_AGENT_ID={agent_id} to your .env file")
            return
        else:
            logger.error("Failed to create agent")
            return
    
    # Start the webhook server
    try:
        logger.info("Starting webhook server...")
        await start_webhook_server()
        
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Error running application: {e}")

def generate_video_from_image(image_path, seed=0, cfg_scale=1.8, motion_bucket_id=127):
    url = "https://api.stability.ai/v2beta/image-to-video"
    headers = {
        "authorization": f"Bearer {STABILITY_API_KEY}"
    }
    files = {
        "image": open(image_path, "rb")
    }
    data = {
        "seed": seed,
        "cfg_scale": cfg_scale,
        "motion_bucket_id": motion_bucket_id
    }
    response = requests.post(url, headers=headers, files=files, data=data)
    files["image"].close()

    if response.status_code == 200:
        result = response.json()
        generation_id = result.get("id")
        print("Generation started. ID:", generation_id)
        return generation_id
    else:
        print("Error:", response.text)
        return None

# Example usage:
# generation_id = generate_video_from_image("gtest_image.png")

if __name__ == "__main__":
    asyncio.run(main())