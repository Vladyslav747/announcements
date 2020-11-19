import json
import datetime
import uuid
import os

import boto3
from cerberus import Validator


DEFAULT_SCAN_LIMIT = 10

get_announcements_schema = {
    'limit': {'type': 'integer', 'default': DEFAULT_SCAN_LIMIT, 'coerce': int},
    'last_key': {'type': 'string'}
}

create_announcement_schema = {
    'title': {'type': 'string', 'required': True},
    'description': {'type': 'string', 'required': True}
}


def get_announcements(event, context):
    query_params = event['queryStringParameters'] or {}
    validator = Validator(get_announcements_schema)
    if not validator.validate(query_params):
        return {
            'statusCode': 400,
            'body': json.dumps({'errors': validator.errors})
        }

    cleaned_data = validator.normalized(validator.document)
    table = init_announcements_table()
    scan_params = get_scan_parameters(cleaned_data)
    scan_result = table.scan(**scan_params)
    del scan_result['ResponseMetadata']
    return {
        'statusCode': 200,
        'body': json.dumps(scan_result)
    }


def create_announcement(event, context):
    validator = Validator(create_announcement_schema)
    body_params = json.loads(event['body'] or '{}')
    if not validator.validate(body_params):
        return {
            'statusCode': 400,
            'body': json.dumps({'errors': validator.errors})
        }

    table = init_announcements_table()
    table.put_item(Item=get_announcement_attributes(validator.document))
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'Success'})
    }


def get_user_token(event, context):
    client = boto3.client('cognito-idp')
    user_pool_id = os.environ.get('COGNITO_USER_POOL_ID')
    client_id = os.environ.get('COGNITO_CLIENT_ID')
    params = event['queryStringParameters']
    email, password = params.get('email'), params.get('password')
    params = {
        'UserPoolId': user_pool_id,
        'ClientId': client_id,
        'AuthFlow': 'ADMIN_USER_PASSWORD_AUTH',
        'AuthParameters': {
            'USERNAME': email,
            'PASSWORD': password
        }}
    try:
        response = client.admin_initiate_auth(**params)
    except client.exceptions.UserNotFoundException:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'User does not exist'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'id_token': response['AuthenticationResult']['IdToken']})
    }


def init_announcements_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table('announcements')


def get_scan_parameters(cleaned_data):
    last_key, limit = cleaned_data.get('last_key'), cleaned_data.get('limit')
    scan_params = {'Limit': limit}
    if last_key:
        scan_params['ExclusiveStartKey'] = {'id': last_key}
    return scan_params


def get_announcement_attributes(cleaned_data):
    title, description = cleaned_data['title'], cleaned_data['description']
    date, id_ = str(datetime.datetime.now()), str(uuid.uuid4())
    return {
        'title': title,
        'description': description,
        'date': date,
        'id': id_
    }
