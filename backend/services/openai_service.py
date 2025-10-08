"""
Azure OpenAI Service for meme generation.
Handles communication with Azure OpenAI for text generation.

Enterprise Best Practice: Always log API calls for audit trails and debugging.
"""

import logging
from typing import Dict, Any
from openai import AzureOpenAI
from config import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for interacting with Azure OpenAI."""
    
    def __init__(self):
        """Initialize Azure OpenAI client."""
        self.client = AzureOpenAI(
            api_key=settings.azure_openai_api_key,
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint
        )
        self.deployment_name = settings.azure_openai_text_deployment_name
    
    async def generate_meme_text(self, topic: str, mood: str = "funny") -> Dict[str, Any]:
        """
        Generate meme text based on topic and mood.
        
        Args:
            topic: The subject matter for the meme
            mood: The desired tone (funny, sarcastic, wholesome, etc.)
        
        Returns:
            Dict containing the generated meme text and metadata
        
        Raises:
            Exception: If OpenAI API call fails
        """
        try:
            system_prompt = (
                "You are a creative meme generator for workplace morale. "
                "Generate short, witty, and appropriate meme text that would work well "
                "with popular meme formats. Keep it professional yet fun."
            )
            
            user_prompt = f"Create a {mood} meme about: {topic}"
            
            logger.info(f"Generating meme for topic: {topic}, mood: {mood}")
            logger.info(f"Using deployment: {self.deployment_name}")
            logger.info(f"Using endpoint: {settings.azure_openai_endpoint}")
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=150,
                temperature=0.8,  # Higher temperature for more creative outputs
            )
            
            meme_text = response.choices[0].message.content
            
            logger.info("Meme text generated successfully")
            
            return {
                "text": meme_text,
                "topic": topic,
                "mood": mood,
                "model": self.deployment_name,
                "finish_reason": response.choices[0].finish_reason
            }
            
        except Exception as e:
            logger.error(f"Error generating meme text: {str(e)}")
            logger.error(f"Deployment name used: {self.deployment_name}")
            logger.error(f"Endpoint used: {settings.azure_openai_endpoint}")
            raise Exception(f"Failed to generate meme: {str(e)}")
    
    async def generate_meme_suggestion(self, topic: str) -> Dict[str, str]:
        """
        Generate a meme format suggestion based on the topic.
        
        Returns:
            Dict with top_text and bottom_text for classic meme format
        """
        try:
            system_prompt = (
                "You are a meme expert. Given a topic, suggest top and bottom text "
                "for a classic two-line meme format. Return ONLY the two lines, "
                "separated by a pipe character (|). Example: 'WHEN YOU CODE|IT WORKS FIRST TRY'"
            )
            
            user_prompt = f"Topic: {topic}"
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=100,
                temperature=0.9,
            )
            
            meme_lines = response.choices[0].message.content.strip()
            
            # Parse the response
            if "|" in meme_lines:
                top, bottom = meme_lines.split("|", 1)
            else:
                # Fallback if format isn't followed
                lines = meme_lines.split("\n")
                top = lines[0] if len(lines) > 0 else meme_lines
                bottom = lines[1] if len(lines) > 1 else ""
            
            return {
                "top_text": top.strip(),
                "bottom_text": bottom.strip()
            }
            
        except Exception as e:
            logger.error(f"Error generating meme suggestion: {str(e)}")
            raise Exception(f"Failed to generate meme suggestion: {str(e)}")
