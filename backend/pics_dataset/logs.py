import logging

from fan_tools.fan_logging import setup_logger

from .config import config


setup_logger('pics_dataset', config.LOG_DIR)
log = logging.getLogger('app')
