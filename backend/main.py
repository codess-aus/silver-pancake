"""
FastAPI backend for Silver Pancake - AI Meme Generator with Responsible AI
Context: This API orchestrates meme generation using Azure OpenAI with 
enterprise-grade content safety and moderation.

Interesting Fact: FastAPI automatically generates interactive API docs at /docs!
"""

import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

from config import settings
from services.openai_service import OpenAIService
from services.content_safety_service import ContentSafetyService
from services.enhanced_meme_service import EnhancedMemeService

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Request/Response Models
class MemeRequest(BaseModel):
    """Request model for meme generation."""
    topic: str = Field(..., min_length=1, max_length=200, description="Topic for the meme")
    mood: str = Field(default="funny", description="Mood/tone of the meme")


class VisualMemeRequest(BaseModel):
    """Request model for visual meme generation."""
    topic: str = Field(..., min_length=1, max_length=200, description="Topic for the meme")
    mood: str = Field(default="funny", description="Mood/tone of the meme")
    include_text: bool = Field(default=True, description="Include text components")
    include_image: bool = Field(default=True, description="Include visual image")


class MemeResponse(BaseModel):
    """Response model for generated meme."""
    success: bool
    meme_text: Optional[str] = None
    top_text: Optional[str] = None
    bottom_text: Optional[str] = None
    topic: str
    mood: str
    is_safe: bool
    safety_analysis: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


class FeedbackRequest(BaseModel):
    """Request model for user feedback on generated memes."""
    meme_text: str
    reason: str = Field(..., description="Reason for flagging")
    user_comment: Optional[str] = None


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup."""
    logger.info("Starting Silver Pancake API...")
    # app.state.openai_service = OpenAIService()  # Disabled - no text models deployed
    app.state.content_safety_service = ContentSafetyService()
    app.state.enhanced_meme_service = EnhancedMemeService()
    logger.info("Services initialized successfully")
    yield
    logger.info("Shutting down Silver Pancake API...")


# Initialize FastAPI app
app = FastAPI(
    title="Silver Pancake API",
    description="AI Meme Generator with Responsible AI and Content Safety",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """
    Root endpoint for health checks.
    Returns API information and status.
    """
    return {
        "message": "Welcome to Silver Pancake API!",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "healthy"
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "environment": settings.environment}


# Text-based meme endpoint disabled - no text models deployed
# Only visual memes are available with gpt-image-1 deployment
@app.post("/api/generate-meme")
async def generate_meme_redirect(request: MemeRequest):
    """
    Redirect users to visual meme generation.
    Text-based memes are not available as no text models are deployed.
    """
    return {
        "success": False,
        "message": "Text-based memes are not available. Please use /api/generate-visual-meme for image-based memes.",
        "redirect": "/api/generate-visual-meme",
        "available_endpoints": ["/api/generate-visual-meme"],
        "note": "Only visual memes are supported with the current gpt-image-1 deployment."
    }
# @app.post("/api/generate-meme", response_model=MemeResponse)
# async def generate_meme(request: MemeRequest):
#     """
#     Generate a meme with content safety checks.
#     
#     This endpoint:
#     1. Generates meme text using Azure OpenAI
#     2. Analyzes content with Azure Content Safety
#     3. Returns the meme only if it passes safety checks
#     
#     Responsible AI: All content is moderated before being returned to users.
#     """
#     try:
#         logger.info(f"Meme generation requested - Topic: {request.topic}, Mood: {request.mood}")
#         
#         # Generate meme text
#         openai_service = app.state.openai_service
#         meme_data = await openai_service.generate_meme_text(request.topic, request.mood)
#         
#         # Generate structured meme format
#         meme_suggestion = await openai_service.generate_meme_suggestion(request.topic)
#         
#         # Content safety check
#         content_safety_service = app.state.content_safety_service
#         is_safe, safety_results = await content_safety_service.analyze_text(meme_data["text"])
#         
#         if not is_safe:
#             # Log flagged content for evaluation
#             content_safety_service.log_flagged_content(meme_data["text"], safety_results)
#             
#             return MemeResponse(
#                 success=False,
#                 topic=request.topic,
#                 mood=request.mood,
#                 is_safe=False,
#                 safety_analysis=safety_results,
#                 message="Content did not pass safety checks. Please try a different topic."
#             )
#         
#         # Return safe content
#         return MemeResponse(
#             success=True,
#             meme_text=meme_data["text"],
#             top_text=meme_suggestion["top_text"],
#             bottom_text=meme_suggestion["bottom_text"],
#             topic=request.topic,
#             mood=request.mood,
#             is_safe=True,
#             safety_analysis=safety_results,
#             message="Meme generated successfully!"
#         )
#         
#     except Exception as e:
#         logger.error(f"Error in meme generation: {str(e)}")
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed to generate meme: {str(e)}"
#         )


@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackRequest, background_tasks: BackgroundTasks):
    """
    Submit feedback on a generated meme.
    
    Allows users to flag inappropriate content that passed initial checks.
    This feedback is crucial for continuous model evaluation and improvement.
    """
    try:
        logger.info(f"Feedback received - Reason: {feedback.reason}")
        
        # In production, store in database and trigger evaluation pipeline
        background_tasks.add_task(log_feedback, feedback)
        
        return {
            "success": True,
            "message": "Thank you for your feedback. We'll review this content."
        }
        
    except Exception as e:
        logger.error(f"Error processing feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process feedback")


@app.post("/api/generate-visual-meme")
async def generate_visual_meme(request: VisualMemeRequest):
    """
    Generate a visual meme using Azure OpenAI image generation.
    
    This endpoint demonstrates the full power of AI meme creation:
    1. Creates a detailed prompt for meme-style image generation
    2. Uses your deployed gpt-image-1 model
    3. Returns a complete visual meme
    
    Perfect for modern meme culture!
    """
    try:
        logger.info(f"Visual meme generation requested - Topic: {request.topic}, Mood: {request.mood}")
        
        enhanced_service = app.state.enhanced_meme_service
        
        # Generate complete meme package
        meme_result = await enhanced_service.generate_complete_meme(
            topic=request.topic,
            mood=request.mood,
            include_image=request.include_image,
            include_text=request.include_text
        )
        
        if meme_result["success"]:
            return {
                "success": True,
                "topic": request.topic,
                "mood": request.mood,
                "meme_components": meme_result["components"],
                "message": "Visual meme generated successfully! 🎨"
            }
        else:
            return {
                "success": False,
                "topic": request.topic,
                "mood": request.mood,
                "message": "Failed to generate visual meme components",
                "details": meme_result["components"]
            }
        
    except Exception as e:
        logger.error(f"Error in visual meme generation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate visual meme: {str(e)}"
        )


def log_feedback(feedback: FeedbackRequest):
    """Log user feedback for evaluation."""
    logger.warning(
        f"USER FEEDBACK - Reason: {feedback.reason}, "
        f"Comment: {feedback.user_comment}, "
        f"Meme: {feedback.meme_text[:100]}..."
    )
    # In production: Store in database, send to Application Insights, trigger review
