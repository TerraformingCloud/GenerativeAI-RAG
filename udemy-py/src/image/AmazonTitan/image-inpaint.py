import boto3
import json
import base64

client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def get_configuration(inputImage: str):
    return json.dumps({
    "taskType": "INPAINTING",
    "inPaintingParams": {
        "text": "Make the mountain snowy",
        "negativeText": "bad quality, low res",
        "image": inputImage,
        "maskPrompt": "mountain"
    },
    "imageGenerationConfig": {
        "numberOfImages": 1,
        "height": 512,
        "width": 512,
        "cfgScale": 8.0,
        }
})

with open("trek.png", "rb") as f:
    base_image = base64.b64encode(f.read()).decode("utf-8")

response = client.invoke_model(
    body=get_configuration(base_image),
    modelId="amazon.titan-image-generator-v1",
    accept="application/json",
    contentType="application/json")

response_body = json.loads(response.get("body").read())

base64_image = response_body.get("images")[0]

base_64_image = base64.b64decode(base64_image)

file_path = "trek-snowy.png"
with open(file_path, "wb") as f:
    f.write(base_64_image)