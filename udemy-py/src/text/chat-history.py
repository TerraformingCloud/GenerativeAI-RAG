import boto3
import json

client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

history = []

def get_history():
    return "\n".join(history)

def get_configuration():
    return json.dumps({
        "inputText": get_history(),
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
    history.append("User: " +  user_input)
    if user_input.lower() == "exit":
        break
    response = client.invoke_model(
        body=get_configuration(),
        modelId=model_id,
        accept="application/json",
        contentType="application/json")
    response_body = json.loads(response.get('body').read())
    output_text = response_body.get('results')[0].get('outputText').strip()
    print(output_text)
    history.append(output_text)

# Response

"""
Bot: Hello, I am a chatbot. How can I help you?
User: What is the tallest mountain?
Bot: Mount Everest is the tallest mountain in the world, with a peak of 29,031 feet above sea level. It is located in the Himalayas between Nepal and Tibet.
User: What is the second?
Bot: Mount Kailash is the second-tallest mountain in the world, with a peak of 28,169 feet above sea level. It is located in the Himalayas, on the border between China and Tibet.
User: exit
"""