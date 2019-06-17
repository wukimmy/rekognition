import json
import boto3
from urllib.parse import urlparse, parse_qs
from Check import *
import os

bucket = os.environ['BUCKET_NAME']

client=boto3.client('rekognition')

def lambda_handler(event, context):
    message = ""
    status = False
    neg = False
    print(event)
    #parsed = urlparse(event['queryStringParameters'])
    #code  = parse_qs(parsed.query).get('image')[0]
    code = event['queryStringParameters'].get('image')
    image  = code
    photo= image + '.jpg'
    
    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
    textDetections=response['TextDetections']
    
    el = Elements()
    contents = el.getElements()
    for text in textDetections:
        for cont in contents:
            if text['DetectedText'].upper() == "SEM" or text['DetectedText'].upper() == "NÃO" or text['DetectedText'].upper() == "ZERO":
                neg = True
            if text['DetectedText'].lower() == cont:
                status = True
    if status and neg:
        message += '**ESSE PRODUTO NÃO POSSUI LACTOSE**'
    elif status is False:
        message += '**ESSE PRODUTO NÃO POSSUI DESCRIÇÃO**'
    else:
        message += '**ESSE PRODUTO POSSUI LACTOSE**'
    httpStatusCode = '200'
    return {
        "isBase64Encoded": True,
        "statusCode": httpStatusCode,
        "headers": { },
        "multiValueHeaders": { },
        "body": message
    }
    
    
    