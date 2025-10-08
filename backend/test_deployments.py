#!/usr/bin/env python3
"""
Test script to check available Azure OpenAI deployments.
"""
import os
import sys
sys.path.append('.')
from config import settings
from openai import AzureOpenAI

def test_deployments():
    """Test different deployment configurations."""
    
    client = AzureOpenAI(
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version, 
        azure_endpoint=settings.azure_openai_endpoint
    )
    
    print("Testing Azure OpenAI deployments...")
    print(f"Endpoint: {settings.azure_openai_endpoint}")
    print()
    
    # Test image generation with gpt-image-1
    print("1. Testing gpt-image-1 for image generation:")
    try:
        response = client.images.generate(
            model='gpt-image-1',
            prompt='A simple test image of a cat',
            size='1024x1024',
            quality='high',
            n=1
        )
        print("   ✓ gpt-image-1 works for image generation")
        print(f"   ✓ Generated image URL: {response.data[0].url[:50]}...")
    except Exception as e:
        print(f"   ✗ gpt-image-1 failed: {e}")
    
    print()
    
    # Test text generation with common deployment names
    text_models = ['gpt-4o-mini', 'gpt-4o', 'gpt-35-turbo', 'gpt-4', 'gpt-image-1']
    
    for model in text_models:
        print(f"2. Testing {model} for text generation:")
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Say 'hello' in one word"}],
                max_tokens=10
            )
            print(f"   ✓ {model} works for text generation")
            print(f"   ✓ Response: {response.choices[0].message.content}")
            break
        except Exception as e:
            print(f"   ✗ {model} failed: {e}")
    
    print("\nRecommendation:")
    print("- Use gpt-image-1 for visual meme generation")
    print("- Need a text model deployment for text-based memes")
    print("- Or switch to visual-only meme generation")

if __name__ == "__main__":
    test_deployments()