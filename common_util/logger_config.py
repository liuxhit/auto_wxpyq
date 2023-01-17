# coding: utf-8
import logging
from logging import Logger
from logging.config import dictConfig
import os

ROOT_LOG_DIR = './log'
logger_dict = {
    'version': 1,
    'formatters': {
        'default': {'format': '[%(asctime)s] %(levelname)s by [%(process)d] %(name)s:%(funcName)s(%(lineno)d) : %(message)s', },
        'console': {"format": "%(asctime)s: %(levelname)s: %(pathname)s: \n%(message)s\n", },
        'default_bak': {'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s', },
    },
    'handlers': {
        'rotating_file_handler_main': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'filename': os.path.join(ROOT_LOG_DIR, 'main.log'),
            'mode': 'a',
            'maxBytes': 100*1024*1024,
        },
        'console_info': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'console',
            'stream': 'ext://sys.stdout',
        },
        'console_error': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'console',
            'stream': 'ext://sys.stdout',
        },
    },
    # root logger config
    'root': {
        'level': 'INFO',
        'handlers': ['rotating_file_handler_main']
    },
    # other logger config
    'loggers': {
        'main': {
            'level': 'DEBUG',
            'handlers': ['console_info', 'rotating_file_handler_main',],
            'propagate': False,
        },
        'weixin_tool': {
            'level': 'DEBUG',
            'handlers': ['console_info', 'rotating_file_handler_main',],
            'propagate': False,
        },
    }
}


class LoggingMixin:
    """Convenience super-class to have a logger configured with the class name"""

    @property
    def log(self) -> Logger:
        """Returns a logger."""
        try:
            # FIXME: LoggingMixin should have a default _log field.
            return self._log  # type: ignore
        except AttributeError:
            cls = self.__class__
            self._log = get_logger_by_class_name(cls)
            return self._log


class cached_log_property_on_class:
    """https://stackoverflow.com/a/13624858/1280629"""
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        val = self.fget(owner_cls)
        setattr(owner_cls, self.fget.__name__, val)
        return val


def get_logger_by_class_name(cls):
    return logging.getLogger(cls.__module__ + '.' + cls.__name__)


dictConfig(logger_dict)