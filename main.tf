provider "aws" {
  region = var.region
}

variable "region" {
  description = "The AWS region to deploy resources"
  type        = string
  default     = "us-east-1" #Hard code for now whilst playing.
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_exec_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "lambda_policy" {
  name       = "lambda_policy_attachment"
  roles      = [aws_iam_role.lambda_role.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_cloudwatch_policy" {
  name   = "lambda_cloudwatch_policy"
  role   = aws_iam_role.lambda_role.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "lambda_src"
  output_path = "lambda_function.zip"
}

resource "aws_lambda_function" "execute_python" {
  function_name    = "execute_my_lambda_code"
  role            = aws_iam_role.lambda_role.arn
  runtime         = "python3.9"
  handler         = "lambda_function.lambda_handler"
  filename        = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  memory_size     = 128
  timeout         = 5
}

# Create the REST API, it was html but this is better.. I think .
resource "aws_api_gateway_rest_api" "lambda_api" {
  name        = "lambda_api"
  description = "API Gateway for Lambda"
}

resource "aws_api_gateway_resource" "lambda_resource" {
  rest_api_id = aws_api_gateway_rest_api.lambda_api.id
  parent_id   = aws_api_gateway_rest_api.lambda_api.root_resource_id
  path_part   = "execute"
}

resource "aws_api_gateway_method" "lambda_method" {
  rest_api_id   = aws_api_gateway_rest_api.lambda_api.id
  resource_id   = aws_api_gateway_resource.lambda_resource.id
  http_method   = "POST"
  authorization = "NONE"
  api_key_required = true
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.lambda_api.id
  resource_id = aws_api_gateway_resource.lambda_resource.id
  http_method = aws_api_gateway_method.lambda_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.execute_python.invoke_arn
}

#This needs fixing.
resource "aws_api_gateway_deployment" "lambda_deployment" {
  depends_on = [
    aws_api_gateway_integration.lambda_integration,
  ]

  rest_api_id = aws_api_gateway_rest_api.lambda_api.id
  stage_name  = "dev" #Fix me
}

resource "aws_lambda_permission" "apigw_lambda" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.execute_python.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.lambda_api.execution_arn}/*/*"
}

resource "aws_api_gateway_api_key" "lambda_api_key" {
  name        = "lambda_api_key"
  description = "API Key for Lambda execution"
  enabled     = true
}

# Create Usage Plan for the API Key
resource "aws_api_gateway_usage_plan" "lambda_usage_plan" {
  name        = "lambda_usage_plan"
  description = "Usage Plan for Lambda API"

  api_stages {
    api_id = aws_api_gateway_rest_api.lambda_api.id
    stage  = aws_api_gateway_deployment.lambda_deployment.stage_name
  }

  throttle_settings {
    rate_limit  = 10  # Max 10 requests per second
    burst_limit = 20  # Max 20 requests in burst
  }
}

resource "aws_api_gateway_usage_plan_key" "lambda_usage_plan_key" {
  key_id        = aws_api_gateway_api_key.lambda_api_key.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.lambda_usage_plan.id
}

output "api_gateway_url" {
  value = "https://${aws_api_gateway_rest_api.lambda_api.id}.execute-api.${var.region}.amazonaws.com/dev/execute"
  description = "Invoke this URL to call the Lambda function"
}

# Output API Key Value (without sensitive flag to display the key)
output "api_key_value" {
  value = nonsensitive(aws_api_gateway_api_key.lambda_api_key.value)
  description = "Use this API Key to authenticate requests"
}