import json

print("Function Initialization")


def lambda_handler(event, context):
    print("Inside The Handler")
    print("Doing something")

    # raise TypeError
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello, Lambda Extensions!",
        }),
    }
