import json


def generate(event, context):
    request_body = json.loads(event["body"])

    response = {"statusCode": 200, "body": request_body}

    return response
