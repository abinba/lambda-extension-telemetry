import json

print("Function Initialization")


def lambda_handler(event, context):
    print("Inside The Handler")
    print("Hello, Loki!")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello, Loki!",
        }),
    }
