import boto3

client = boto3.client('lambda',
                       region_name='us-east-2')

def invoke_abort_lambda():
    FUNCTION_NAME = 'reset-scraper'

    response = client.invoke(
        FunctionName=FUNCTION_NAME,
        InvocationType='Event'
    )