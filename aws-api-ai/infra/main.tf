terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}  

# Lambda code

data "archive_file" "python_lambda" {
  type = "zip"
  source_file = "./code/lambda_function.py"
  output_path = "pylambda.zip"
}

# Lambda
resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.bedrock.function_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "${aws_api_gateway_rest_api.bedrock.execution_arn}/*"
}

resource "aws_lambda_function" "bedrock" {
  filename      = "pylambda.zip"
  function_name = "bedrockLambda"
  role          = aws_iam_role.role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.11"
  timeout       = 60
  source_code_hash = data.archive_file.python_lambda.output_base64sha256 #filebase64sha256("pylambda.zip")
  lifecycle {
    ignore_changes = [ source_code_hash ]
  }
}

# resource "aws_lambda_invocation" "bedrock" {
#   function_name = aws_lambda_function.bedrock.function_name

#   input = jsonencode({
#     prompt = "Hello, how are you?"
#   })
# }

# IAM
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com", "bedrock.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "role" {
  name               = "lambda-lambdaRole-bedrock"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
} 

resource "aws_api_gateway_rest_api" "bedrock" {
  name        = "Bedrock-Api-GW"
  description = "API GW for Bedrock testing."
}

resource "aws_api_gateway_resource" "bedrock" {
  rest_api_id = aws_api_gateway_rest_api.bedrock.id
  parent_id   = aws_api_gateway_rest_api.bedrock.root_resource_id
  path_part   = "demoBedrock"
}

resource "aws_api_gateway_method" "bedrock" {
  rest_api_id   = aws_api_gateway_rest_api.bedrock.id
  resource_id   = aws_api_gateway_resource.bedrock.id
  http_method   = "POST"
  authorization = "NONE"
  request_parameters = {
    "method.request.querystring.prompt" = true
  }
}

resource "aws_api_gateway_method_response" "bedrock" {
  rest_api_id = aws_api_gateway_rest_api.bedrock.id
  resource_id = aws_api_gateway_resource.bedrock.id
  http_method = aws_api_gateway_method.bedrock.http_method
  status_code = "200"
}

import {
  to = aws_api_gateway_method_response.bedrock
  id = "j41tf0wcli/ewhwns/POST/200"
}

resource "aws_api_gateway_deployment" "bedrock" {
  rest_api_id = aws_api_gateway_rest_api.bedrock.id

  # triggers = {
  #   redeployment = sha1(jsonencode([
  #     aws_api_gateway_resource.bedrock.id,
  #     aws_api_gateway_method.bedrock.id,
  #     aws_api_gateway_integration.bedrock.id])
  #   )
  # }

  lifecycle {
    create_before_destroy = true
  }
}

import {
  to = aws_api_gateway_deployment.bedrock
  id = "j41tf0wcli/z83vmh"
}

resource "aws_api_gateway_stage" "bedrock" {
  deployment_id = aws_api_gateway_deployment.bedrock.id
  rest_api_id   = aws_api_gateway_rest_api.bedrock.id
  stage_name    = "Dev"
}

import {
  to = aws_api_gateway_stage.bedrock
  id = "j41tf0wcli/Dev"
}


resource "aws_api_gateway_integration" "bedrock" {
  rest_api_id          = aws_api_gateway_rest_api.bedrock.id
  resource_id          = aws_api_gateway_resource.bedrock.id
  http_method          = aws_api_gateway_method.bedrock.http_method
  type                 = "AWS"
  integration_http_method = "POST"
  uri = aws_lambda_function.bedrock.invoke_arn
  content_handling        = "CONVERT_TO_TEXT"

  request_templates = {
      "application/json" = jsonencode( 
        {
          prompt = "$input.params('prompt')"
        }
    )
  }
}