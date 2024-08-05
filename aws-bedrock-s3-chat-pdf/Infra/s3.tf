terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.57.0"
    }
  }
}

provider "aws" {
 region = "us-east-1"
 default_tags {
    tags = {
      Environment = "Dev" 
      Project = "Bedrock"
    }
 }
}

resource "aws_s3_bucket" "rag" {
  bucket = "chat-with-pdf-rag"
}
