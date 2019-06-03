import boto3
import json
client = boto3.client('dynamodb')

# class Elements:
#     def getElements(self):
content = []
response = client.scan(
    TableName='nome da tabela',
    Select='SPECIFIC_ATTRIBUTES',
    AttributesToGet=[
        'type'
    ]
)
for i in response['Items']:
    content.append(i['type'])
    a = str(i['type'])
    print(a.split(':',6))
# return content
