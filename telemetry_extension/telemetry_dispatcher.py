import logging
import os

import json

DISPATCH_MIN_BATCH_SIZE = int(os.getenv("DISPATCH_MIN_BATCH_SIZE", 1))

logger = logging.getLogger(__name__)


def dispatch_telemetry(queue, force):
    while (not queue.empty()) and (force or queue.qsize() >= DISPATCH_MIN_BATCH_SIZE):
        batch = queue.get_nowait()
        # Sending every log to Loki
        for log in batch:
            if log["type"] == "function":
                logger.info(json.dumps(log))
