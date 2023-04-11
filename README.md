# loki-lambda-extension

## Description

AWS Lambda extension, written in Python, which allows sending 
telemetry data to Loki, wrapped into the Docker image.

Dockerhub: `railflow/loki-lambda-extension`

Available tags:

- `railflow/loki-lambda-extension:3.7` (Python 3.7)
- `railflow/loki-lambda-extension:3.8` (Python 3.8)
- `railflow/loki-lambda-extension:3.9` (Python 3.9)

## How to use

You can find the example Lambda function written 
in Python in `example` folder.

In order to use this extension you need to wrap your function as an image.
Image recommended to use by AWS for creating Lambda is `public.ecr.aws/lambda/python`.

By default, Lambda launches all the scripts that are located at `/opt/extensions` folder, 
so we should copy the extension files to `/opt/` folder.

**It is obligatory to install `requests` and `python-logging-loki` packages for the extension
to work correctly.**

```
FROM railflow/loki-lambda-extension:3.8 AS layer
FROM public.ecr.aws/lambda/python:3.8

...

WORKDIR /opt
COPY --from=layer /opt/ .

...

RUN python3 -m pip install --upgrade pip &&  \
    python3 -m pip install requests -q && \
    python3 -m pip install python-logging-loki -q

CMD ["handler.handler"]
```

## Environment variables

Those environment variables should be set in AWS Lambda configuration settings for Lambda 
to be able to connect to Loki server.

`LOKI_USER` - User ID in Loki configuration (e.g. 123456) 

`LOKI_HOST` - Host address of the Loki indicated in your account (e.g. logs.grafana.net)

`LOKI_API_KEY` - API Key used for authorization

## Results

Lambda extension works based on the Lambda function states: 
- INIT
- INVOKE
- SHUTDOWN <- shutdown time can vary, so all the logs before the shutdown and invoke will be shown with delay

From the observations, it can take up to 2-5 minutes for all the logs to show up in Loki.

## Example

In the `example` folder we are using **Pulumi** Infrastructure-As-Code tool to deploy the function code to the Lambda.

## References

[Official example](https://github.com/aws-samples/aws-lambda-extensions/tree/main/python-example-telemetry-api-extension) 
for Python Telemetry API Extension by AWS was used as the base of the code.

