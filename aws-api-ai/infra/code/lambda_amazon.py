import boto3
import json

bedrock_client = boto3.client(service_name='bedrock-runtime')


def lambda_handler(event, context):
    input_prompt=event['prompt']
    print(input_prompt)

    request_body = json.dumps({
        "inputText": input_prompt,
        "textGenerationConfig": {
            "maxTokenCount": 100,
            "stopSequences": [],
            "temperature": 0,
            "topP": 1
        }
    })

    request = bedrock_client.invoke_model(
        contentType='application/json',
        accept='application/json',
        modelId='amazon.titan-text-express-v1',
        body=request_body
    )

    #print(request)

    response_body = json.loads(request.get('body').read())
    
    #print(response_body)
    
    response = response_body.get('results')[0].get('outputText')
    
    print(response)
    
    return{
        'statusCode': 200,
        'body': json.dumps(response)
    }