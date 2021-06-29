## Provision AWS API-Gateway with Lambda's that handle Okta webhooks.

https://developer.okta.com/docs/reference/api/event-types/#catalog

1. Init Serverless Framework on local machine:
```
curl -o- -L https://slss.io/install | bash
```

2. Deploy Lambda function, API-gateway, SNS-topic.
(Write down automatically generated endpoints and API Keys)
```
cd okta-lambda
sls config credentials -p aws -k <AWS_KEY> -s <AWS_SECRET> -o
sls deploy
```

3. Check locally:
```
serverless invoke local -f UserCreate -p event-user-activate-auth.json
```

4. Login to OKTA admin and create Hooks:
```
	Admin -> Workflow -> Event Hooks:
	Create event:
		Name: StreamToSNS
		URL: Endpoint from SLS-deploy step
		Authentication field: x-api-key
		Authentication secret: API Keys from SLS-deploy step
		Subscribe to events: User.*
```

5. Check function logs:
```
sls logs -f StreamToSNS -t
```