#!/usr/bin/env python3
"""
Test script specifically for your gpt-image-1 deployment.
This will verify that image generation works correctly.
"""

import os
import sys
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

def test_image_generation():
    """Test image generation with your deployed model."""
    
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    image_deployment = os.getenv("AZURE_OPENAI_IMAGE_DEPLOYMENT_NAME", "gpt-image-1")
    
    print("🖼️ Testing Azure OpenAI Image Generation")
    print("=" * 50)
    print(f"Endpoint: {endpoint}")
    print(f"Image Deployment: {image_deployment}")
    print(f"API Version: {api_version}")
    print()
    
    try:
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )
        
        print("✅ Client created successfully")
        print("🎨 Generating test meme image...")
        
        # Test with a simple meme prompt
        response = client.images.generate(
            model=image_deployment,
            prompt="A funny office meme about coding bugs, internet meme style, workplace humor, safe for work",
            size="1024x1024",
            quality="high",
            n=1
        )
        
        image_url = response.data[0].url
        
        print(f"✅ SUCCESS! Image generated!")
        print(f"🔗 Image URL: {image_url}")
        print()
        print("🎉 Your gpt-image-1 model is working perfectly!")
        print("👉 We can now generate visual memes with Silver Pancake!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing image generation: {str(e)}")
        
        if "404" in str(e):
            print("💡 The deployment name might be incorrect.")
        elif "401" in str(e):
            print("💡 Check your API key.")
        elif "quota" in str(e).lower():
            print("💡 You may have hit your usage quota.")
        
        return False

if __name__ == "__main__":
    success = test_image_generation()
    if success:
        print("\n🚀 Ready to generate visual memes!")
    else:
        print("\n❌ Need to fix the configuration first.")
        sys.exit(1)