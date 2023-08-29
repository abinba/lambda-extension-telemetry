import logging
import os
import requests
import json

logger = logging.getLogger(__name__)

TELEMETRY_API_URL = "http://{0}/2022-07-01/telemetry".format(os.getenv("AWS_LAMBDA_RUNTIME_API"))
LAMBDA_EXTENSION_IDENTIFIER_HEADER_KEY = "Lambda-Extension-Identifier"

TIMEOUT_MS = 1000  # Maximum time (in milliseconds) that a batch is buffered.
MAX_BYTES = 256 * 1024  # Maximum size in bytes that the logs are buffered in memory.
MAX_ITEMS = 10000  # Maximum number of events that are buffered in memory.


def subscribe_listener(extension_id, listener_url):
    logger.debug(
        "Subscribing Extension to receive telemetry data. "
        "ExtenionsId: {0}, "
        "listener url: {1}, "
        "telemetry api url: {2}".format(extension_id, listener_url, TELEMETRY_API_URL)
    )

    try:
        subscription_request_body = {
            "schemaVersion": "2022-07-01",
            "destination": {
                "protocol": "HTTP",
                "URI": listener_url,
            },
            "types": ["platform", "function", "extension"],
            "buffering": {
                "timeoutMs": TIMEOUT_MS,
                "maxBytes": MAX_BYTES,
                "maxItems": MAX_ITEMS
            }
        };

        subscription_request_headers = {
            "Content-Type": "application/json",
            LAMBDA_EXTENSION_IDENTIFIER_HEADER_KEY: extension_id,
        }

        response = requests.put(
            TELEMETRY_API_URL,
            data=json.dumps(subscription_request_body),
            headers=subscription_request_headers
        )

        if response.status_code == 200:
            logger.debug(f"Extension successfully subscribed to telemetry api {response.text}")
        elif response.status_code == 202:
            logger.debug("Telemetry API not supported. Are you running the extension locally?")
        else:
            logger.debug(
                "Subscription to telemetry API failed. "
                f"Status code: {response.status_code}, response text: {response.text}"
            )
        return extension_id

    except Exception as e:
        logger.debug(f"Error registering extension: {e}")
        raise Exception("Error setting AWS_LAMBDA_RUNTIME_API", e)
