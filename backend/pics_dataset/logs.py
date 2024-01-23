import logging

from fan_tools.fan_logging import setup_logger

from .context_vars import app_config


def setup_logging():
    log_dir = app_config.get().LOG_DIR
    log_dir.mkdir(exist_ok=True, parents=True)
    setup_logger('pics_dataset', log_dir)
    log = logging.getLogger('app')
