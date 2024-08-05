import boto3
import json
import pprint

client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

titan_model_id = 'amazon.titan-text-express-v1'

titan_config = json.dumps({
    "inputText": "what is the tallest mountain on Earth?",
    "textGenerationConfig": {
        "maxTokenCount": 8192,
        "stopSequences": [],
        "temperature": 0,
        "topP": 1
    }
})

response = client.invoke_model(
    body=titan_config,
    modelId=titan_model_id,
    accept="application/json",
    contentType="application/json"
)

response_body = json.loads(response.get('body').read())
pp = pprint.PrettyPrinter(depth=4)

pp.pprint(response_body.get('results'))

# Meta - LLAMA MODEL

# llama_model_id = 'meta.llama3-8b-instruct-v1:0'

# llama_config = json.dumps({
#     "prompt": "what is the tallest mountain on Earth?",
#     "max_gen_len": 512,
#     "temperature": 0.5,
#     "top_p": 0.9
# })

# response = client.invoke_model(
#     body=llama_config,
#     modelId=llama_model_id,
#     accept="application/json",
#     contentType="application/json"
# )

# response_body = json.loads(response.get('body').read())

# pp = pprint.PrettyPrinter(depth=4)

# pp.pprint(response_body["generation"])

