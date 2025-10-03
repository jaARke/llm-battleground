import atexit
import logging
import queue
import sys
from logging.handlers import QueueHandler, QueueListener


def init_logging() -> None:
    # Set up queue-based logging
    log_queue: queue.Queue = queue.Queue()
    queue_handler = QueueHandler(log_queue)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    logger.addHandler(queue_handler)

    # Add console handler
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )

    # Start the queue listener
    queue_listener = QueueListener(log_queue, console_handler)
    queue_listener.start()

    # Register atexit handler to stop the listener
    atexit.register(queue_listener.stop)
