import boto3

client = boto3.client('lex-models')

response = client.create_bot_version(
    name='OfficeBot'
    )

print(response)