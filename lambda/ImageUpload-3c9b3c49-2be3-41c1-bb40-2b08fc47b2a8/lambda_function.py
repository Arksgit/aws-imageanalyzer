import json
import boto3
import base64
import uuid

s3 = boto3.client('s3')
BUCKET_NAME = "image-analyzer-s3"

def lambda_handler(event, context):

    try:
        body = json.loads(event.get('body', '{}'))
        file_data = body.get('file')

        if not file_data:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No file provided'})
            }

        file_data += "=" * (-len(file_data) % 4)
        file_content = base64.b64decode(file_data)

        file_name = f"uploads/{uuid.uuid4()}.jpg"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=file_content,
            ContentType='image/jpeg'
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Upload successful',
                'file': file_name
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }