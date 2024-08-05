import boto3
import json

client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def get_configuration(prompt:str):
    return json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 4096,
            "stopSequences": [],
            "temperature": 0,
            "topP": 1
        }
    })

print(
    "Bot: Hello, I am a chatbot. How can I help you?"
)

model_id = 'amazon.titan-text-express-v1'

while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break
    response = client.invoke_model(
        body=get_configuration(user_input),
        modelId=model_id,
        accept="application/json",
        contentType="application/json")
    response_body = json.loads(response.get('body').read())
    print(response_body.get('results')[0].get('outputText'))

# Response

"""
Bot: Hello, I am a chatbot. How can I help you?
User: Tell me a joke # User Input

Why did the scarecrow win an award?

It was outstanding in its field.

User: exit

"""