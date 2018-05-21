# import os

from decouple import config
from unipath import Path
import dj_database_url

BASE_DIR = Path(__file__).parent

SECRET_KEY = config('SECRET_KEY', default='doesntmatter')

DEBUG = config('DEBUG', default=False, cast=bool)

INSTALLED_APPS = [
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    # 'django.contrib.staticfiles',

    'buildhub.main',
    'buildhub.ingest',
]


DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='postgresql://localhost/buildhub2',
        cast=dj_database_url.parse
    )
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Home-butchered
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': config('DJANGO_LOG_LEVEL', 'INFO'),
#         },
#         'boto3': {
#             'handlers': ['console'],
#             'level': config('BOTO3_LOG_LEVEL', 'INFO'),
#         },
#         'botocore': {
#             'handlers': ['console'],
#             'level': config('BOTOCORE_LOG_LEVEL', 'INFO'),
#         },
#
#     },
# }

# Basic dockerflow
# LOGGING = {
#     'version': 1,
#     'formatters': {
#         'json': {
#             '()': 'dockerflow.logging.JsonLogFormatter',
#             'logger_name': 'myproject'
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'json'
#         },
#     },
#     'loggers': {
#         'request.summary': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     }
# }

# Dockerflow from Tecken
LOGGING_USE_JSON = config('LOGGING_USE_JSON', True, cast=bool)

LOGGING_DEFAULT_LEVEL = config('LOGGING_DEFAULT_LEVEL', 'INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'dockerflow.logging.JsonLogFormatter',
            'logger_name': 'buildhub',
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': LOGGING_DEFAULT_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': (
                'json' if LOGGING_USE_JSON else 'verbose'
            ),
        },
        'sentry': {
            'level': 'ERROR',
            'class': (
                'raven.contrib.django.raven_compat.handlers'
                '.SentryHandler'
            ),
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['sentry', 'console'],
    },
    'loggers': {
        'django': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.request': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'buildhub': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'markus': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'request.summary': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    },
}

SQS_QUEUE_URL = config('SQS_QUEUE_URL')

# For more details, see:
# http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Queue.receive_messages

# The duration (in seconds) for which the call waits for a message
# to arrive in the queue before returning.
SQS_QUEUE_WAIT_TIME_SECONDS = config(
    'SQS_QUEUE_WAIT_TIME_SECONDS', cast=int, default=10
)
# The duration (in seconds) that the received messages are hidden
# from subsequent retrieve requests after being retrieved by
# a ReceiveMessage request.
SQS_QUEUE_VISIBILITY_TIMEOUT = config(
    'SQS_QUEUE_VISIBILITY_TIMEOUT', cast=int, default=5,
)
# The maximum number of messages to return.
# Valid values are 1 to 10. Default is 1.
SQS_QUEUE_MAX_NUMBER_OF_MESSAGES = config(
    'SQS_QUEUE_MAX_NUMBER_OF_MESSAGES', cast=int, default=1,
)


# if 'AWS_ACCOUNT_ID' not in os.environ:
#     # The reason for doing this is because sqs_listener can't run at all
#     # if you haven't set os.environ['AWS_ACCOUNT_ID'].
#     # That means you need to always set it on the command line and you
#     # can't benefit from the .env file that decouple can use.
#     os.environ['AWS_ACCOUNT_ID'] = config('AWS_ACCESS_KEY_ID')
