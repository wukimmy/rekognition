import boto3

client = boto3.client('dynamodb')

response = client.scan(
    TableName='Nome da tabela',
    Select='SPECIFIC_ATTRIBUTES',
    AttributesToGet=[
        'Filtro'
    ]
    
)

print(response);