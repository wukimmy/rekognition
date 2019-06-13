import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tablename')

class Elements:
        def getElements(self):
            response = table.scan();
            items = response['Items'];
            contentlist =[]
            for item in items:
                contentlist.append(item['intem name on table'])
            return contentlist

