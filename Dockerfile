FROM public.ecr.aws/lambda/python:3.12

# Copy the resource_feedback_summarization module
# COPY resource_feedback_summarization/ ${LAMBDA_TASK_ROOT}/resource_feedback_summarization

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

RUN pip install psycopg2-binary

# Copy function code
COPY . ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "main.lambda_handler" ]