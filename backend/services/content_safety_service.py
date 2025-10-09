"""
Azure Content Safety Service for content moderation.
Evaluates generated content for safety and appropriateness.

Responsible AI Best Practice: Always moderate AI-generated content before 
displaying it to users, especially in enterprise environments.
"""

import logging
from typing import Dict, Any, Tuple
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, AnalyzeImageOptions, ImageData
from config import settings
import base64

logger = logging.getLogger(__name__)


class ContentSafetyService:
    """Service for content moderation using Azure Content Safety API."""
    
    # Severity levels: 0 (safe) to 6 (severe)
    SEVERITY_THRESHOLD = 2  # Reject content with severity >= 2
    
    def __init__(self):
        """Initialize Azure Content Safety client."""
        self.client = ContentSafetyClient(
            endpoint=settings.azure_content_safety_endpoint,
            credential=AzureKeyCredential(settings.azure_content_safety_api_key)
        )
    
    async def analyze_text(self, text: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Analyze text for safety issues.
        
        Args:
            text: The text content to analyze
        
        Returns:
            Tuple of (is_safe: bool, analysis_results: Dict)
            
        Interesting Fact: Azure Content Safety checks for hate, sexual, 
        violence, and self-harm content in multiple languages!
        """
        try:
            logger.info("Analyzing content for safety")
            
            request = AnalyzeTextOptions(text=text)
            response = self.client.analyze_text(request)
            
            # Extract category results
            results = {
                "hate": {
                    "severity": response.hate_result.severity if response.hate_result else 0,
                },
                "self_harm": {
                    "severity": response.self_harm_result.severity if response.self_harm_result else 0,
                },
                "sexual": {
                    "severity": response.sexual_result.severity if response.sexual_result else 0,
                },
                "violence": {
                    "severity": response.violence_result.severity if response.violence_result else 0,
                }
            }
            
            # Determine if content is safe
            is_safe = all(
                category["severity"] < self.SEVERITY_THRESHOLD 
                for category in results.values()
            )
            
            # Find the highest severity category if unsafe
            if not is_safe:
                max_category = max(results.items(), key=lambda x: x[1]["severity"])
                results["flagged_category"] = max_category[0]
                results["max_severity"] = max_category[1]["severity"]
                logger.warning(
                    f"Content flagged: {max_category[0]} "
                    f"(severity: {max_category[1]['severity']})"
                )
            else:
                logger.info("Content passed safety checks")
            
            results["is_safe"] = is_safe
            results["threshold"] = self.SEVERITY_THRESHOLD
            
            return is_safe, results
            
        except Exception as e:
            logger.error(f"Error analyzing content safety: {str(e)}")
            # Fail closed: if safety check fails, reject the content
            return False, {
                "error": str(e),
                "is_safe": False,
                "message": "Safety analysis failed - content rejected as precaution"
            }
    
    async def analyze_image(self, image_data: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Analyze image for safety issues.
        
        Args:
            image_data: Base64-encoded image data (with or without data URI prefix)
        
        Returns:
            Tuple of (is_safe: bool, analysis_results: Dict)
            
        Enterprise Best Practice: Always moderate AI-generated images before
        displaying them to users, especially in workplace environments.
        """
        try:
            logger.info("Analyzing image for safety")
            
            # Remove data URI prefix if present
            if image_data.startswith('data:image'):
                # Extract just the base64 part after the comma
                image_data = image_data.split(',', 1)[1]
            
            # Decode base64 to bytes
            image_bytes = base64.b64decode(image_data)
            
            # Create image analysis request
            request = AnalyzeImageOptions(image=ImageData(content=image_bytes))
            response = self.client.analyze_image(request)
            
            # Parse categories_analysis - it's a list of dictionaries
            # e.g., [{'category': 'Hate', 'severity': 0}, {'category': 'SelfHarm', 'severity': 0}, ...]
            cat_analysis = response.categories_analysis
            results = {
                "hate": {"severity": 0},
                "self_harm": {"severity": 0},
                "sexual": {"severity": 0},
                "violence": {"severity": 0}
            }
            
            # Map the categories from the API response to our result structure
            for category_result in cat_analysis:
                category_name = category_result.get('category', '').lower()
                severity = category_result.get('severity', 0)
                
                if category_name == 'hate':
                    results["hate"]["severity"] = severity
                elif category_name == 'selfharm':
                    results["self_harm"]["severity"] = severity
                elif category_name == 'sexual':
                    results["sexual"]["severity"] = severity
                elif category_name == 'violence':
                    results["violence"]["severity"] = severity
            
            # Determine if content is safe
            is_safe = all(
                category["severity"] < self.SEVERITY_THRESHOLD 
                for category in results.values()
            )
            
            # Find the highest severity category if unsafe
            if not is_safe:
                max_category = max(results.items(), key=lambda x: x[1]["severity"])
                results["flagged_category"] = max_category[0]
                results["max_severity"] = max_category[1]["severity"]
                logger.warning(
                    f"Image flagged: {max_category[0]} "
                    f"(severity: {max_category[1]['severity']})"
                )
            else:
                logger.info("Image passed safety checks")
            
            results["is_safe"] = is_safe
            results["threshold"] = self.SEVERITY_THRESHOLD
            results["content_type"] = "image"
            
            return is_safe, results
            
        except Exception as e:
            logger.error(f"Error analyzing image safety: {str(e)}")
            logger.error(f"Error details: {repr(e)}")
            # Fail closed: if safety check fails, reject the content
            return False, {
                "error": str(e),
                "is_safe": False,
                "content_type": "image",
                "message": "Image safety analysis failed - content rejected as precaution"
            }
    
    def log_flagged_content(self, text: str, analysis_results: Dict[str, Any]) -> None:
        """
        Log flagged content for review and evaluation.
        
        Enterprise Best Practice: Maintain audit logs of flagged content
        for compliance, model evaluation, and continuous improvement.
        """
        content_type = analysis_results.get('content_type', 'text')
        logger.warning(
            f"FLAGGED {content_type.upper()} - Category: {analysis_results.get('flagged_category', 'unknown')}, "
            f"Severity: {analysis_results.get('max_severity', 'N/A')}"
        )
        
        if content_type == 'text':
            logger.warning(f"Text preview: {text[:100]}...")
        
        # In production, you would:
        # 1. Store in a database for review
        # 2. Send to Azure Application Insights
        # 3. Trigger alerts if needed
        # 4. Feed into evaluation pipelines
