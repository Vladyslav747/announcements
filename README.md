# Announcements microservice

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- core - Code for the application's Lambda functions.
- events - Invocation events that you can use to invoke the function.
- tests - Unit tests for the application code. 
- template.yaml - A template that defines the application's AWS resources.
- openapi.yaml - OpenAPI 3.0 specification

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project.

## Documentation

* Join the [postman workspace](https://app.getpostman.com/join-team?invite_code=9f092f5c5d31b810b2574fe31f20dde4) and poke around in the collection which includes some tests and a monitor.
* Techonoligies stack choices [explained](https://docs.google.com/document/d/1XU3lYmYrJxCW6KSSRM8_55XcjMaF65_Q5zBYaH5t2ps/edit?usp=sharing)

## Deploy the application
In order to access the private API you must have a user in your Cognito user pool and obtain a user token.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

## Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
sam-app$ sam build --use-container
```

The SAM CLI installs dependencies defined in `hello_world/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
sam-app$ sam local invoke HelloWorldFunction --event events/event.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
sam-app$ sam local start-api
sam-app$ curl http://localhost:3000/
```