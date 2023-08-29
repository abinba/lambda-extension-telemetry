import logging
import os
import sys
import requests
import json

logger = logging.getLogger(__name__)

LAMBDA_EXTENSION_NAME_HEADER_KEY = "Lambda-Extension-Name"
LAMBDA_EXTENSION_IDENTIFIER_HEADER_KEY = "Lambda-Extension-Identifier"
REGISTRATION_REQUEST_BASE_URL = "http://{0}/2020-01-01/extension".format(os.getenv("AWS_LAMBDA_RUNTIME_API"))


def register_extension(extension_name):
    logger.debug(f"Registering Extension using {REGISTRATION_REQUEST_BASE_URL}")

    try:
        registration_request_body = {
            "events":
                [
                    "INVOKE", "SHUTDOWN"
                ]
        }
        registration_request_header = {
            "Content-Type": "application/json",
            LAMBDA_EXTENSION_NAME_HEADER_KEY: extension_name,
        }

        response = requests.post(
            "{0}/register".format(REGISTRATION_REQUEST_BASE_URL),
            data=json.dumps(registration_request_body),
            headers=registration_request_header
        )

        if response.status_code == 200:
            extension_id = response.headers[LAMBDA_EXTENSION_IDENTIFIER_HEADER_KEY]
            logger.info(f"Registration success with extensionId {extension_id}")
        else:
            logger.error(f"Error registering logging extension: {response.text}")
            # Fail the extension
            sys.exit(1)

        return extension_id

    except Exception as e:
        logger.error(f"Error registering logging extension: {e}")
        raise Exception("Error setting AWS_LAMBDA_RUNTIME_API", e)


def next_event(extension_id):
    try:
        next_event_request_header = {
            "Content-Type": "application/json",
            LAMBDA_EXTENSION_IDENTIFIER_HEADER_KEY: extension_id,
        }

        response = requests.get(
            "{0}/event/next".format(REGISTRATION_REQUEST_BASE_URL),
            headers=next_event_request_header
        )

        if response.status_code != 200:
            logger.error(f"Failed receiving next event {response.status_code} {response.text}")
            # Fail extension with non-zero exit code
            sys.exit(1)

        event_data = response.json()
        return event_data

    except Exception as e:
        logger.error(f"Error registering extension: {e}")
        raise Exception("Error setting AWS_LAMBDA_RUNTIME_API", e)
