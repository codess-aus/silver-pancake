# Install required packages: `pip install requests pillow azure-identity`
import os
import requests
import base64
from PIL import Image
from io import BytesIO
from azure.identity import DefaultAzureCredential

# You will need to set these environment variables or edit the following values.
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://trustworthyai.cognitiveservices.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-image-1")
api_version = os.getenv("OPENAI_API_VERSION", "2025-04-01-preview")

def decode_and_save_image(b64_data, output_filename):
  image = Image.open(BytesIO(base64.b64decode(b64_data)))
  image.show()
  image.save(output_filename)

def save_response(response_data, filename_prefix):
  for idx, item in enumerate(response_data['data']):
    b64_img = item['b64_json']
    filename = f"{filename_prefix}_{idx+1}.png"
    decode_and_save_image(b64_img, filename)
    print(f"Image saved to: '{filename}'")

# Initialize the DefaultAzureCredential to be used for Entra ID authentication.
# If you receive a `PermissionDenied` error, be sure that you run `az login` in your terminal
# and that you have the correct permissions to access the resource.
# Learn more about necessary permissions:  https://aka.ms/azure-openai-roles
credential = DefaultAzureCredential()
token_response = credential.get_token("https://cognitiveservices.azure.com/.default")

base_path = f'openai/deployments/{deployment}/images'
params = f'?api-version={api_version}'

generation_url = f"https://trustworthyai.cognitiveservices.azure.com/{base_path}/generations{params}"
generation_body = {
  "prompt": "<IMAGE_PROMPT>",
  "n": 1,
  "size": "1024x1024",
  "quality": "medium",
  "output_format": "png"
}
generation_response = requests.post(
  generation_url,
  headers={
    'Authorization': 'Bearer ' + token_response.token,
    'Content-Type': 'application/json',
  },
  json=generation_body
).json()
save_response(generation_response, "generated_image")

# In addition to generating images, you can edit them.
edit_url = f"{endpoint}{base_path}/edits{params}"
edit_body = {
  "prompt": "<IMAGE_PROMPT>",
  "n": 1,
  "size": "1024x1024",
  "quality": "medium"
}
files = {
  "image": ("generated_image_1.png", open("generated_image_1.png", "rb"), "image/png"),
  # You can use a mask to specify which parts of the image you want to edit.
  # The mask must be the same size as the input image.
  # "mask": ("mask.png", open("mask.png", "rb"), "image/png"),
}
edit_response = requests.post(
  edit_url,
  headers={'Authorization': 'Bearer ' + token_response.token},
  data=edit_body,
  files=files
).json()
save_response(edit_response, "edited_image")