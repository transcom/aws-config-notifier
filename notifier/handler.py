import json
import logging
import logging.config
import sys

from pythonjsonlogger import jsonlogger

# setup module wide logger

HANDLER = logging.StreamHandler(stream=sys.stdout)
LOGGER = logging.getLogger('notifier')
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(HANDLER)

from notifier.notifier import compliance_notify

def handler(event, context):
    """
    Incoming Lambda Hander
    """
    LOGGER.info('running aws config notifier...')
    compliance_notify()


if __name__ == '__main__':
    handler(None, None)