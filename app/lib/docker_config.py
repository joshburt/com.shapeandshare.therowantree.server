# Allow over-riding the defaults with non-secure ENV variables, or secure docker secrets

import therowantree_config as default_config
import os


###############################################################################
# Direcrtory Options
###############################################################################
LOGS_DIR = default_config.LOGS_DIR
if 'LOGS_DIR' in os.environ:
    LOGS_DIR = os.environ['LOGS_DIR']

TMP_DIR = default_config.TMP_DIR
if 'TMP_DIR' in os.environ:
    TMP_DIR = os.environ['TMP_DIR']

###############################################################################
# Server Options
###############################################################################
API_ACCESS_KEY = default_config.API_ACCESS_KEY
if 'API_ACCESS_KEY' in os.environ:
    API_ACCESS_KEY = os.environ['API_ACCESS_KEY']

API_VERSION = default_config.API_VERSION
if 'API_VERSION' in os.environ:
    API_VERSION = os.environ['API_VERSION']

LISTENING_HOST = default_config.LISTENING_HOST
if 'LISTENING_HOST' in os.environ:
    LISTENING_HOST = os.environ['LISTENING_HOST']

FLASK_DEBUG = default_config.FLASK_DEBUG
if 'FLASK_DEBUG' in os.environ:
    FLASK_DEBUG = bool(os.environ['FLASK_DEBUG'])

###############################################################################
#  Database Options
###############################################################################
API_DATABASE_SERVER = default_config.API_DATABASE_SERVER
if 'API_DATABASE_SERVER' in os.environ:
    API_DATABASE_SERVER = os.environ['API_DATABASE_SERVER']

API_DATABASE_NAME = default_config.API_DATABASE_NAME
if 'API_DATABASE_NAME' in os.environ:
    API_DATABASE_NAME = os.environ['API_DATABASE_NAME']

API_DATABASE_USERNAME = default_config.API_DATABASE_USERNAME
if 'API_DATABASE_USERNAME' in os.environ:
    API_DATABASE_USERNAME = os.environ['API_DATABASE_USERNAME']

API_DATABASE_PASSWORD = default_config.API_DATABASE_PASSWORD
if 'API_DATABASE_PASSWORD' in os.environ:
    API_DATABASE_PASSWORD = os.environ['API_DATABASE_PASSWORD']
