import logging
import time

from pathlib import Path
from queue import Queue

from extensions_api_client import register_extension, next_event
from logging_config import setup_logging, LOKI_API_KEY, SESSION_UUID
from telemetry_http_listener import start_http_listener
from telemetry_api_client import subscribe_listener
from telemetry_dispatcher import dispatch_telemetry


logger = logging.getLogger(__name__)


def main():
    if not LOKI_API_KEY:
        return

    setup_logging(debug=False, session_uuid=SESSION_UUID)
    logger.info("Starting the Telemetry API Extension")

    extension_name = Path(__file__).parent.name
    logger.debug("Extension Main: Registring the extension using extension name: {0}".format(extension_name))
    extension_id = register_extension(extension_name)

    logger.debug("Extension Main: Starting the http listener which will receive data from Telemetry API")
    queue = Queue()
    listener_url = start_http_listener(queue)

    logger.debug("Extension Main: Subscribing the listener to TelemetryAPI")
    subscribe_listener(extension_id, listener_url)

    while True:
        logger.debug("Extension Main: Next")

        event_data = next_event(extension_id=extension_id)
        logger.debug(f"Received event: {event_data}")

        if event_data["eventType"] == "INVOKE":
            logger.debug("Extension Main: Handle Invoke Event")
            dispatch_telemetry(queue, False)
        elif event_data["eventType"] == "SHUTDOWN":
            # Wait for 1 sec to receive remaining events
            time.sleep(2)
            logger.info("Shutdown initialized")
            dispatch_telemetry(queue, True)
            # sys.exit(0)
            break


if __name__ == "__main__":
    main()
