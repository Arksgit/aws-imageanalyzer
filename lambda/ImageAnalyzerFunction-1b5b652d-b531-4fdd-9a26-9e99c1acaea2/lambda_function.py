import json
import boto3
import urllib.parse
import datetime

rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ImageLabels')

def lambda_handler(event, context):

    print("EVENT:", event)

    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

        print("Processing:", key)

        response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            },
            MaxLabels=5,
            MinConfidence=80
        )

        labels = [label['Name'] for label in response['Labels']]

        print("Labels:", labels)

        table.put_item(
            Item={
                'ImageName': key,
                'DetectedLabels': labels,
                'Timestamp': str(datetime.datetime.now())
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps(labels)
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            'statusCode': 500,
            'body': str(e)
        }