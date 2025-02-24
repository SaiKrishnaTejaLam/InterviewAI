# **Interview Questions Generator Lambda Service**

## **Overview**

This AWS Lambda service generates interview questions based on a provided job description (JD). It utilizes OpenAI's GPT-4 model to generate 20 relevant questions. The service is triggered by an API call and supports CORS.

## **Architecture**

* AWS Lambda  
* AWS Secrets Manager  
* Bitbucket CI/CD Pipeline  
* OpenAI API

## **Workflow**

1. An API call triggers the Lambda function.  
2. The function retrieves OpenAI API keys and a prompt template from AWS Secrets Manager.  
3. The job description is extracted from the request body.  
4. The prompt template is formatted with the job description and sent to OpenAI.  
5. The generated questions are returned in a structured JSON response.

## **Environment Variables**

* `SECRET_NAME`: Name of the secret in AWS Secrets Manager (default: `interviewai_voicecall_questions_service`)  
* `ALLOWED_ORIGIN`: Allowed CORS origin (default: `*`)

## **AWS Secrets Manager Keys**

* `open_ai_key`: API key for OpenAI  
* `prompt`: Template for generating interview questions

## **API Request Format**

{  
  "job\_description": "Software Engineer with expertise in Python and AWS."  
}

## **API Response Format**

{  
  "questions": \[  
    "What are your strengths in Python?",  
    "How have you used AWS services in your previous role?",  
    ...  
  \]  
}

## **CI/CD Pipeline (Bitbucket)**

This project follows a CI/CD pipeline in Bitbucket, triggered when a pull request is merged into the `dev` branch. The pipeline automates:

* Code linting and validation  
* Deployment of the updated Lambda function

### **Bitbucket Pipeline Example (`bitbucket-pipelines.yml`)**

## **Deployment**

1. Push changes to any feature branch.  
2. Create a pull request (PR) to merge into `dev`.  
3. When the PR is merged, the Bitbucket pipeline automatically deploys the Lambda function.

## **Logging and Monitoring**

* AWS CloudWatch logs are enabled for debugging.  
* Errors are logged using Python's `logging` module.

