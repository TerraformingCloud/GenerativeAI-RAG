import boto3
import pprint

bedrock = boto3.client(
    service_name='bedrock',
    region_name='us-east-1')

pp = pprint.PrettyPrinter(depth=4)

# List all foundational models in the region


def list_foundation_models():
    models = bedrock.list_foundation_models()
    for model in models["modelSummaries"]:
        pp.pprint(model)
        pp.pprint("-----------------------------")

list_foundation_models()

# Get a single model

def get_foundation_model(modelIdentifier):
    model = bedrock.get_foundation_model(modelIdentifier=modelIdentifier)
    pp.pprint(model)

get_foundation_model('amazon.titan-text-lite-v1:0:4k')