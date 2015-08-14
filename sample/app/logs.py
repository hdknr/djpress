# -*- coding: utf-8 -*-
#
import os
# import syslog
#
__all__ = ['LOGGING', ]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# See:
#  - http://docs.djangoproject.com/en/dev/topics/logging
#
# - level -
# DEBUG     : Low level system information for debugging purposes
# INFO      : General system information
# WARNING   : Information describing a minor problem that has occurred.
# ERROR     : Information describing a major problem that has occurred.
# CRITICAL  : Information describing a critical problem that has occurred.


_LOG_DIR = os.environ.get(
    'LOGGING_DIR',
    os.path.join(os.path.abspath(BASE_DIR), 'logs'))

if not os.path.isdir(_LOG_DIR):
    os.makedirs(_LOG_DIR)

_LOG_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')


def _P(signature):
    return os.path.join(_LOG_DIR, signature + ".log")


def _F(signature, level='DEBUG'):
    return {
        'level': level,
        'class': 'app.logs.AppFileLogHandler',
        'formatter': 'parsefriendly',
        'when': 'midnight',     # 'when': 'S', 'interval':  2,
        'filename': _P(signature),
    }

_LOG_FORMATTERS = {'parsefriendly': {
    'format': '[%(levelname)s] %(asctime)s - M:%(pathname)s, MSG:%(message)s',
    'datefmt': '%d/%b/%Y:%H:%M:%S %z',
}, }

_LOG_FILTERS = {
    'require_debug_false': {
        '()': 'django.utils.log.RequireDebugFalse'
    }
}

_LOG_HANDLER_MAIL_ADMINS = {
    'level': 'ERROR',
    'filters': ['require_debug_false'],
    'class': 'django.utils.log.AdminEmailHandler'
}


_LOG_ROOT = {
    'handlers': ['file'],
    'level': _LOG_LEVEL,
    'propagate': True
}

from logging.handlers import TimedRotatingFileHandler


class AppFileLogHandler(TimedRotatingFileHandler):
    def doRollover(self):
        super(AppFileLogHandler, self).doRollover()


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'handlers': {
        'mail_admins': _LOG_HANDLER_MAIL_ADMINS,
        'file': _F('apps'),
        'django': _F('django'),
    },

    'formatters': _LOG_FORMATTERS,
    'filters': _LOG_FILTERS,

    'root': _LOG_ROOT,

    'loggers': {
        'django.request': {
            'handlers': ['django'], 'level': 'DEBUG',
        },

        'django.db.backends': {
            'handlers': ['django'], 'level': 'DEBUG',
        },
    },
}
