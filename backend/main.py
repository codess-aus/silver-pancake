"""
FastAPI backend for Silver Pancake
Context: This API will serve as the bridge between your frontend and Azure/OpenAI services.
Interesting Fact: FastAPI automatically generates interactive API docs at /docs!

"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend-backend communication during development.
# Note: In production, restrict origins for security!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only; specify domains in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """
    Root endpoint for health checks.
    Returns a welcome message.
    """
    return {"message": "Welcome to Silver Pancake FastAPI backend!"}
