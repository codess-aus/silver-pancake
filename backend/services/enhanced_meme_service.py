"""
Enhanced Meme Service that generates both text and visual memes.
Demonstrates the full power of Azure OpenAI for creative content generation.

Enterprise Best Practice: Offer multiple content formats to meet diverse user needs.
"""

import logging
from typing import Dict, Any, Optional
from openai import AzureOpenAI
from config import settings

logger = logging.getLogger(__name__)


class EnhancedMemeService:
    """Service for generating both text and visual memes using Azure OpenAI."""
    
    def __init__(self):
        """Initialize Azure OpenAI client for both text and image generation."""
        self.client = AzureOpenAI(
            api_key=settings.azure_openai_api_key,
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint
        )
        self.text_deployment = settings.azure_openai_text_deployment_name
        self.image_deployment = settings.azure_openai_image_deployment_name
    
    async def generate_visual_meme(self, topic: str, mood: str = "funny") -> Dict[str, Any]:
        """
        Generate a complete visual meme with image and text.
        
        Args:
            topic: The subject matter for the meme
            mood: The desired tone (funny, sarcastic, wholesome, etc.)
        
        Returns:
            Dict containing the generated meme image URL and metadata
        """
        try:
            # Create a detailed prompt for meme image generation
            image_prompt = self._create_meme_image_prompt(topic, mood)
            
            logger.info(f"Generating visual meme for topic: {topic}, mood: {mood}")
            logger.info(f"Using image deployment: {self.image_deployment}")
            
            # Generate the meme image
            response = self.client.images.generate(
                model=self.image_deployment,
                prompt=image_prompt,
                size="1024x1024",
                quality="high",
                n=1
            )
            
            image_url = response.data[0].url
            
            logger.info("Visual meme generated successfully")
            
            return {
                "image_url": image_url,
                "prompt": image_prompt,
                "topic": topic,
                "mood": mood,
                "model": self.image_deployment,
                "type": "visual_meme"
            }
            
        except Exception as e:
            logger.error(f"Error generating visual meme: {str(e)}")
            raise Exception(f"Failed to generate visual meme: {str(e)}")
    
    async def generate_text_meme(self, topic: str, mood: str = "funny") -> Dict[str, Any]:
        """
        Generate meme text content for classic meme formats.
        
        Args:
            topic: The subject matter for the meme
            mood: The desired tone
        
        Returns:
            Dict containing meme text and structured format
        """
        try:
            # For now, we'll create a simple text-based response since text model might not be deployed
            # In a full implementation, this would use the text deployment
            
            meme_texts = {
                "coding": {
                    "funny": "When you finally fix that bug... but create three new ones",
                    "sarcastic": "Oh great, another 'simple' feature request",
                    "motivational": "Every bug is just an opportunity to learn something new!"
                },
                "meetings": {
                    "funny": "This meeting could have been an email... but here we are",
                    "sarcastic": "Let's circle back on synergizing our paradigm shifts",
                    "motivational": "Great minds collaborate to achieve amazing things!"
                }
            }
            
            # Simple fallback text generation
            default_text = f"When you're dealing with {topic}... it's definitely {mood}!"
            meme_text = meme_texts.get(topic.lower(), {}).get(mood, default_text)
            
            return {
                "text": meme_text,
                "top_text": f"WHEN YOU'RE DEALING WITH {topic.upper()}",
                "bottom_text": "IT'S ALWAYS AN ADVENTURE",
                "topic": topic,
                "mood": mood,
                "type": "text_meme"
            }
            
        except Exception as e:
            logger.error(f"Error generating text meme: {str(e)}")
            raise Exception(f"Failed to generate text meme: {str(e)}")
    
    def _create_meme_image_prompt(self, topic: str, mood: str) -> str:
        """
        Create a detailed prompt for meme image generation.
        
        This is where the magic happens - crafting prompts that generate
        recognizable meme-style images with workplace themes.
        """
        
        base_style = "internet meme style, bold text overlay, high contrast, "
        
        mood_styles = {
            "funny": "humorous, lighthearted, cartoonish, bright colors",
            "sarcastic": "deadpan expression, muted colors, ironic situation", 
            "wholesome": "warm, friendly, positive vibes, soft lighting",
            "motivational": "inspiring, energetic, success-oriented, dynamic pose",
            "relatable": "everyday situation, realistic, 'this is so me' feeling"
        }
        
        topic_scenes = {
            "coding": "developer at computer, multiple monitors, coffee cup, late night coding",
            "meetings": "conference room, people around table, video call screen, presentation",
            "coffee": "office coffee machine, tired employee, morning routine, coffee cup",
            "deadlines": "stressed worker, clock showing time pressure, papers scattered",
            "debugging": "frustrated programmer, error messages on screen, rubber duck",
            "teamwork": "collaborative workspace, people working together, brainstorming"
        }
        
        # Build the complete prompt
        style = mood_styles.get(mood, mood_styles["funny"])
        scene = topic_scenes.get(topic.lower(), f"workplace situation involving {topic}")
        
        prompt = f"{base_style}{style}, {scene}, meme format, professional workplace setting, safe for work content"
        
        # Add text overlay instruction
        prompt += f", with space for text overlay about {topic} in a {mood} way"
        
        return prompt
    
    async def generate_complete_meme(self, topic: str, mood: str = "funny", 
                                   include_image: bool = True, 
                                   include_text: bool = True) -> Dict[str, Any]:
        """
        Generate a complete meme package with both visual and text elements.
        
        This is the premium meme generation experience!
        """
        try:
            result = {
                "topic": topic,
                "mood": mood,
                "timestamp": logger.name,  # Using logger.name as placeholder
                "components": {}
            }
            
            if include_image:
                try:
                    visual_result = await self.generate_visual_meme(topic, mood)
                    result["components"]["visual"] = visual_result
                except Exception as e:
                    logger.warning(f"Visual meme generation failed: {e}")
                    result["components"]["visual"] = {"error": str(e)}
            
            if include_text:
                try:
                    text_result = await self.generate_text_meme(topic, mood)
                    result["components"]["text"] = text_result
                except Exception as e:
                    logger.warning(f"Text meme generation failed: {e}")
                    result["components"]["text"] = {"error": str(e)}
            
            # Determine success
            result["success"] = len([c for c in result["components"].values() if "error" not in c]) > 0
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating complete meme: {str(e)}")
            raise Exception(f"Failed to generate complete meme: {str(e)}")