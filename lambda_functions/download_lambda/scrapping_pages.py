import json
import boto3
import urllib.request

def lambda_handler(event, context):
    url = 'https://www.eltiempo.com/'
    
    with urllib.request.urlopen(url) as response:
        html = response.read()
    
    s3_client = boto3.client('s3')
    s3_client.put_object(
        Body=html,
        Bucket='bigdata2023hugoespinosa',
        Key='index.html',
        ContentType='text/html'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
