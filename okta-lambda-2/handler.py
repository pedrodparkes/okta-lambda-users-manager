# https://developer.okta.com/docs/reference/api/event-types/#catalog
# Main Lambda push events to SNS
# Disable users in Gitlab, Artifactory, Atlassian (Crowd).
# Create usesr in Gitlab, Artifactory, Atlassian to run user disable on they behalf

import os
import json
import boto3
from botocore.exceptions import ClientError

debug = os.environ['DEBUG']
print(debug)

def UserCreate(event, context):
    if debug == 'true':
        print(json.dumps(event))
    request_body=json.loads(event['body'])
    eventType=request_body['data']['events'][0]['eventType']                # 'user.lifecycle.create'
    eventNown=request_body['data']['events'][0]['target'][0]['type']        # 'User'
    userId=request_body['data']['events'][0]['target'][0]['alternateId']    # 'john@gmail.com'
    userName=request_body['data']['events'][0]['target'][0]['displayName']  # 'John Doe'
    if debug == 'true':
        if eventType == 'user.lifecycle.create':
            print("Created user: "+str(userId)+"  "+str(userName))
        elif eventType == 'user.lifecycle.activate':
            print("Activated user: "+str(userId)+"  "+str(userName))
        elif eventType == 'user.lifecycle.reactivate':
            print("Reactivated user: "+str(userId)+"  "+str(userName))
        elif eventType == 'user.lifecycle.unsuspend':
            print("Unsuspended user: "+str(userId)+"  "+str(userName))
        else:
            print("Unrecognized Event")

    return {"statusCode": 200}

def UserDelete(event, context):
    if debug == 'true':
        print(json.dumps(event))
    request_body=json.loads(event['body'])
    eventType=request_body['data']['events'][0]['eventType']                # 'user.lifecycle.create'
    eventNown=request_body['data']['events'][0]['target'][0]['type']        # 'User'
    userId=request_body['data']['events'][0]['target'][0]['alternateId']    # 'john@gmail.com'
    userName=request_body['data']['events'][0]['target'][0]['displayName']  # 'John Doe'
    if debug == 'true':
        if eventType == 'user.lifecycle.delete.initiated':
            print("Deleted user: "+str(userId)+"  "+str(userName))
        elif eventType == 'user.lifecycle.deactivate':
            print("Deactivated user: "+str(userId)+"  "+str(userName))
        elif eventType == 'user.lifecycle.suspend':
            print("Suspended user: "+str(userId)+"  "+str(userName))
        else:
            print("Unrecognized Event")

    return {"statusCode": 200}

def StreamToSNS(event, context):
    sns_topic_arn = os.environ['SNS_TOPIC_ARN']
    client = boto3.client('sns')
    if debug == 'true':
        print(json.dumps(event))
    request_body=json.loads(event['body'])
    eventType=request_body['data']['events'][0]['eventType']                # 'user.lifecycle.create'
    eventNown=request_body['data']['events'][0]['target'][0]['type']        # 'User'
    userId=request_body['data']['events'][0]['target'][0]['alternateId']    # 'john@gmail.com'
    userName=request_body['data']['events'][0]['target'][0]['displayName']  # 'John Doe'
    if debug == 'true':
        if   eventType == 'user.lifecycle.create':
            print("Created user: "+str(userId)+"  "+str(userName))
        elif eventType == 'user.lifecycle.activate':
            print("Activated user: "+str(userId)+"  "+str(userName))
        elif eventType == 'user.lifecycle.reactivate':
            print("Reactivated user: "+str(userId)+"  "+str(userName))
        elif eventType == 'user.lifecycle.unsuspend':
            print("Unsuspended user: "+str(userId)+"  "+str(userName))
        elif eventType == 'user.lifecycle.delete.initiated':
            print("Deleted user: "+str(userId)+"  "+str(userName))
        elif eventType == 'user.lifecycle.deactivate':
            print("Deactivated user: "+str(userId)+"  "+str(userName))
        elif eventType == 'user.lifecycle.suspend':
            print("Suspended user: "+str(userId)+"  "+str(userName))
        else:
            print("Unrecognized Event")
            exit(1)

    try:
        sns_message=json.dumps({"default": str(eventType), "userId": str(userId), "userName": userName})
        response = client.publish(
            TopicArn=sns_topic_arn,
            Message=sns_message,
            MessageStructure='json',
        )
        print("Pushed to SNS topic "+str(sns_topic_arn)+"\n"+str(sns_message))
    except:
        print("SNS Push Failed")

    return {"statusCode": 200}

def Verify(event, context):
    payload=event
    try:
        verification_value_from_header=payload["headers"]["X-Okta-Verification-Challenge"]
        print("X-Okta-Verification-Challenge: "+str(verification_value_from_header))
        body = {
            "statusCode": 200,
            "body": json.dumps({"verification": verification_value_from_header}),
            "headers": {
              "Content-Type": "application/json"
            }
        }
    except:
        print("X-Okta-Verification-Challenge: NOT FOUND!")
        body = {
            "statusCode": 200,
            "body": json.dumps({"verification": "Not Found"}),
            "headers": {
              "Content-Type": "application/json"
            }
        }
    return body