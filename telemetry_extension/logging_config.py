import logging
import os

import logging_loki
import sys

LOKI_USER = os.getenv("LOKI_USER")
LOKI_API_KEY = os.getenv("LOKI_API_KEY")
LOKI_HOST = os.getenv("LOKI_HOST")
LOKI_PUSH_URI = f"https://{LOKI_USER}:{LOKI_API_KEY}@{LOKI_HOST}/loki/api/v1/push"
SESSION_UUID = os.getenv("SESSION_UUID", "NOT_DEFINED")


def setup_logging(
    debug: bool = False,
    session_uuid=None,
):
    level = logging.DEBUG if debug else logging.INFO

    handlers = []
    logging_loki.emitter.LokiEmitter.level_tag = "level"
    handler = logging_loki.LokiHandler(
        url=LOKI_PUSH_URI,
        tags={"service": "blazetest", "session_id": session_uuid},
        version="1",
    )
    handlers.append(handler)
    handlers.append(logging.StreamHandler(stream=sys.stdout))

    logging.basicConfig(
        format="%(process)d-%(levelname)s-[%(filename)s:%(lineno)d]-%(message)s",
        level=level,
        handlers=handlers,
    )
