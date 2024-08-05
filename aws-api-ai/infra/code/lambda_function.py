import boto3
import json

bedrock_client = boto3.client(service_name='bedrock-runtime')


def lambda_handler(event, context):
    input_prompt=event['prompt']
    print(input_prompt)

    request_body = json.dumps({
        "prompt": input_prompt,
        "max_tokens": 100,
        "temperature": 0.8
    })

    request = bedrock_client.invoke_model(
        contentType='application/json',
        accept='application/json',
        modelId='cohere.command-light-text-v14',
        body=request_body
    )

    #print(request)

    response_byte = request['body'].read()

    #print(response_byte)

    response_string = json.loads(response_byte)

    #print(response_string)

    response = response_string['generations'][0]['text']

    print(response)

    return{
        'statusCode': 200,
        'body': json.dumps(response)
    }