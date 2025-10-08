#!/usr/bin/env python3
"""
Quick utility to check available Azure OpenAI deployments.
This helps debug deployment name issues.
"""

import os
import sys
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

def check_deployments():
    """Check available deployments in the Azure OpenAI resource."""
    
    # Get configuration
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    print("🔍 Azure OpenAI Configuration Check")
    print("=" * 50)
    print(f"Endpoint: {endpoint}")
    print(f"API Version: {api_version}")
    print(f"Deployment Name: {deployment_name}")
    print()
    
    if not all([endpoint, api_key]):
        print("❌ Missing Azure OpenAI credentials!")
        return False
    
    try:
        # Create client
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )
        
        print("✅ Azure OpenAI client created successfully")
        
        # Try to use the specified deployment
        print(f"\n🧪 Testing deployment: {deployment_name}")
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "user", "content": "Say 'Hello, this is a test!'"}
            ],
            max_tokens=50
        )
        
        print(f"✅ Deployment '{deployment_name}' works!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Error testing deployment '{deployment_name}': {str(e)}")
        
        # Try common deployment names including the original one
        common_names = ["gpt-image-1", "gpt-4", "gpt-35-turbo", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini"]
        
        print(f"\n🔍 Trying common deployment names...")
        
        for name in common_names:
            try:
                response = client.chat.completions.create(
                    model=name,
                    messages=[
                        {"role": "user", "content": "Test"}
                    ],
                    max_tokens=10
                )
                print(f"✅ '{name}' works!")
                print(f"   👉 Update AZURE_OPENAI_DEPLOYMENT_NAME={name}")
                return name
                
            except Exception as test_e:
                print(f"❌ '{name}' failed: {str(test_e)[:100]}...")
        
        print(f"\n💡 Suggestions:")
        print(f"1. Check your Azure OpenAI resource in the Azure portal")
        print(f"2. Go to 'Model deployments' section")
        print(f"3. Verify the deployment name matches exactly")
        print(f"4. Ensure the model is deployed and running")
        
        return False

if __name__ == "__main__":
    result = check_deployments()
    if not result:
        sys.exit(1)