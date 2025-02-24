import os
import boto3
import json
import logging
import openai

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_secret(secret_name):
    """
    Retrieve a secret from AWS Secrets Manager.
    """
    client = boto3.client("secretsmanager")
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response["SecretString"])
        return secret
    except Exception as e:
        logger.error(f"Error retrieving secret {secret_name}: {e}")
        return None


def create_response(status_code, body):
    """
    Helper function to create a JSON response with CORS headers.
    """
    allowed_origin = os.environ.get("ALLOWED_ORIGIN", "*") 

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": allowed_origin,
            "Access-Control-Allow-Methods": "OPTIONS, POST",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    """
    AWS Lambda handler for generating interview questions using OpenAI's API.
    """
    print(f"Received Event : {event}")

    # Handle CORS preflight requests
    if event.get("httpMethod") == "OPTIONS":
        return create_response(200, {"message": "CORS preflight response"})

    # Retrieve secrets
    secret_name = os.environ.get("SECRET_NAME", "interviewai_voicecall_questions_service")
    secrets = get_secret(secret_name)

    if not secrets:
        logger.error("Failed to retrieve secrets.")
        return create_response(500, {"error": "Failed to retrieve secrets."})

    openai_api_key = secrets.get("open_ai_key")
    prompt_template = secrets.get("prompt")

    if not openai_api_key or not prompt_template:
        logger.error("Missing required keys in secrets.")
        return create_response(500, {"error": "Missing required keys in secrets."})

    # Extract and parse body safely
    body = event.get("body")
    job_description = None

    if body:
        try:
            body = json.loads(body)  # Decode JSON body
            job_description = body.get("job_description")
        except json.JSONDecodeError:
            logger.error("Invalid JSON format in the body.")
            return create_response(400, {"error": "Invalid JSON format in the body."})

    if not job_description:
        logger.warning("Job description is missing in the event.")
        return create_response(400, {"error": "Job description is required in the event."})

    # Format the prompt with the job description
    formatted_prompt = prompt_template.replace("{job description}", job_description)

    try:
        openai.api_key = openai_api_key
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an interviewer."},
                {"role": "user", "content": formatted_prompt},
            ],
        )

        questions = response["choices"][0]["message"]["content"].strip()

        return create_response(200, {"questions": questions})

    except Exception as e:
        logger.error(f"Error processing OpenAI API request: {e}")
        return create_response(500, {"error": str(e)})
