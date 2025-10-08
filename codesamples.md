
1. Authentication using API Key
For Serverless API Endpoints, deploy the Model to generate the endpoint URL and an API key to authenticate against the service. In this sample endpoint and key are strings holding the endpoint URL and the API Key. The API endpoint URL and API key can be found on the Deployments + Endpoint page once the model is deployed.

If you're using bash:

export AZURE_API_KEY="<your-api-key>"

If you're in powershell:

$Env:AZURE_API_KEY = "<your-api-key>"

If you're using Windows command prompt:

set AZURE_API_KEY = <your-api-key>

2. Run a basic code sample
To generate an image, paste the following into a shell

curl -X POST "https://trustworthyai.cognitiveservices.azure.com/openai/deployments/gpt-image-1/images/generations?api-version=2025-04-01-preview" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_API_KEY" \
  -d '{
     "prompt" : "A photograph of a red fox in an autumn forest",
     "size" : "1024x1024",
     "quality" : "medium",
     "output_compression" : 100,
     "output_format" : "png",
     "n" : 1
    }' | jq -r '.data[0].b64_json' | base64 --decode > generated_image.png

To edit an image, paste the following into a shell

curl -X POST "https://trustworthyai.cognitiveservices.azure.com/openai/deployments/gpt-image-1/images/edits?api-version=2025-04-01-preview" \
  -H "Authorization: Bearer $AZURE_API_KEY" \
  -F "image=@image_to_edit.png" \
  -F "mask=@mask.png" \
  -F "prompt=Make this black and white"  | jq -r '.data[0].b64_json' | base64 --decode > edited_image.png