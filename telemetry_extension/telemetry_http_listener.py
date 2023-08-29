import logging
import os
import sys
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Event, Thread

logger = logging.getLogger(__name__)

LISTENER_ADDRESS = "0.0.0.0" if os.getenv("AWS_SAM_LOCAL") else "sandbox.localdomain"
LISTENER_PORT = 4243


def start_http_listener(queue):
    def request_handler(*args):
        TelemetryRequestHandler(queue, *args)

    logger.debug(f"Starting http listener on {LISTENER_ADDRESS}:{LISTENER_PORT}")
    http_server = HTTPServer((LISTENER_ADDRESS, LISTENER_PORT), request_handler)

    started_event = Event()
    server_thread = Thread(target=run_server, daemon=True, args=(started_event, http_server, ))
    server_thread.start()

    is_event_started = started_event.wait(timeout=9)
    if not is_event_started:
        logger.error("server_thread has timed out before starting")
        raise Exception("server_thread has timed out before starting")

    logger.debug("Started http listener")
    listener_url = "http://{0}:{1}".format(LISTENER_ADDRESS,LISTENER_PORT)
    return listener_url


# Server thread
def run_server(started_event, http_server):
    # Notify that this thread is up and running
    started_event.set()
    try:
        http_server.serve_forever()
    except Exception as e:
        logger.error(f"Error in HTTP server {sys.exc_info()[0]}")
        raise Exception("Error in HTTP server", e)
    finally:
        if http_server:
            http_server.shutdown()


class TelemetryRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, queue, *args):
        self.queue = queue
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_POST(self):
        try:
            cl = self.headers.get("Content-Length")
            if cl:
                data_len = int(cl)
            else:
                data_len = 0
            content = self.rfile.read(data_len)
            self.send_response(200)
            self.end_headers()
            batch = json.loads(content.decode("utf-8"))
            self.queue.put(batch)

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            raise Exception("Error processing message", e)

