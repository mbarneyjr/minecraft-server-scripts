import os
import json
import base64
from datetime import datetime
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv('JOBS_TABLE'))


def string_to_base64(value):
    return base64.b64encode(value.encode('utf-8')).decode('utf-8')


def base64_to_string(value):
    return base64.b64decode(value).decode('utf-8')


def lambda_response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body, default=str),
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': '*',
        },
    }


def get_recent_jobs(start_key = None):
    params = {
        'KeyConditionExpression': '#id = :id',
        'FilterExpression': 'NOT #status = :status',
        'ExpressionAttributeNames': {
            '#id': 'id',
            '#status': 'status',
        },
        'ExpressionAttributeValues': {
            ':id': 'JOB',
            ':status': 'COMPLETED',
        },
        'ScanIndexForward': False,
    }
    if start_key:
        params['ExclusiveStartKey'] = start_key
    response = table.query(**params)
    return response


def create_job(event, context):
    print('Event', json.dumps(event, default=str))
    jobs = get_recent_jobs().get('Items')
    if jobs:
        return lambda_response(400, {'jobs': jobs})

    created_at = datetime.now().isoformat()
    job = {
        'id': 'JOB',
        'createdAt': created_at,
        'lastUpdated': created_at,
        'status': 'REQUESTED',
    }
    table.put_item(Item=job)
    return lambda_response(200, {'job': job})


def list_jobs(event, context):
    print('Event', json.dumps(event, default=str))
    qs_params = event.get('queryStringParameters') or {}
    next_token = json.loads(base64_to_string(qs_params.get('nextToken'))) if 'nextToken' in qs_params else None
    response = get_recent_jobs(next_token)
    jobs = response.get('Items', [])
    last_key = string_to_base64(json.dumps(response['LastEvaluatedKey'])) if 'LastEvaluatedKey' in response else None
    return lambda_response(200, {'jobs': jobs, 'nextToken': last_key})


def update_job(event, context):
    print('Event', json.dumps(event, default=str))
    path_params = event.get('pathParameters') or {}
    job_created_at = path_params.get('createdAt')
    body = event.get('body') or '{}'
    update = json.loads(body)
    last_updated_at = datetime.now().isoformat()
    status = update.get('status')
    percent = update.get('percent')

    response = table.update_item(
        Key={'id': 'JOB', 'createdAt': job_created_at},
        UpdateExpression='set #status = :status, #percent = :percent',
        ExpressionAttributeNames={
            '#status': 'status',
            '#percent': 'percent',
        },
        ExpressionAttributeValues={
            ':status': status,
            ':percent': percent,
        },
        ReturnValues='ALL_NEW',
    )
    return lambda_response(200, {'job': response.get('Attributes')})
