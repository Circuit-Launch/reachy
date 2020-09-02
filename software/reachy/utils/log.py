"""
Log utility module.

Provides base Formatter and default configuration.
The default behavior can be overriden using the settings.py file.

"""

import logging
import importlib

from datetime import datetime
from pythonjsonlogger import jsonlogger


class JsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON Formatter to simplify log analysis."""

    def add_fields(self, log_record, record, message_dict):
        """Add timestamp and level in the log_record."""
        jsonlogger.JsonFormatter.add_fields(
            self,
            log_record,
            record,
            message_dict
        )

        log_record['name'] = record.name
        log_record['level'] = record.levelname

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        log_record['timestamp'] = now


DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'precise': {
            'class': 'logging.Formatter',
            'format': '{asctime}:{name}:{levelname}: {message}',
            'style': '{',
        },
        'json-precise': {
            '()': 'reachy.utils.log.JsonFormatter',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/tmp/reachy.log',
            'mode': 'w',
            'formatter': 'json-precise',
        },
    },
    'loggers': {
        'reachy': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}


def configure_logging(logging_config, logging_settings):
    """Configure Reacy logging system as defined by the settings file."""
    module_path, class_name = logging_config.rsplit('.', 1)
    logging_config_func = getattr(importlib.import_module(module_path), class_name)

    logging.config.dictConfig(DEFAULT_LOGGING)

    if logging_settings:
        logging_config_func(logging_settings)