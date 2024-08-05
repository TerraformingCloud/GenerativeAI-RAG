import boto3
import json
import base64

client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

stability_image_config = json.dumps({
    "text_prompts": [
        {
            "text": 'A photo of batman',
        }
    ],
    "height": 512,
    "weight": 512,
    "cfg_scale": 10,
    "style_preset": '3d-model',
})

response = client.invoke_model(
    body=stability_image_config,
    modelId='stability.stable-diffusion-xl-v1',
    accept="application/json",
    contentType="application/json")

response_body = json.loads(response.get("body").read())

base64_image = response_body.get("artifacts")[0].get("base64")

base_64_image = base64.b64decode(base64_image)

file_path = "batman.png"
with open(file_path, "wb") as f:
    f.write(base_64_image)