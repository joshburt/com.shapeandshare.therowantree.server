import ConfigParser

my_config = ConfigParser.ConfigParser()
configFilePath = r'./therowantree.config'
my_config.read(configFilePath)

###############################################################################
# Direcrtory Options
###############################################################################
LOGS_DIR = my_config.get('DIRECTORY', 'logs_dir')
TMP_DIR = my_config.get('DIRECTORY', 'tmp_dir')


###############################################################################
# Server Options
###############################################################################
API_ACCESS_KEY = my_config.get('SERVER', 'api_access_key')
API_VERSION = my_config.get('SERVER', 'api_version')
LISTENING_HOST = my_config.get('SERVER', 'listening_host')
FLASK_DEBUG = my_config.getboolean('SERVER', 'flask_debug')


###############################################################################
# Database Options
###############################################################################
API_DATABASE_SERVER= my_config.get('DATABASE', 'server')
API_DATABASE_NAME = my_config.get('DATABASE', 'database')
API_DATABASE_USERNAME = my_config.get('DATABASE', 'username')
API_DATABASE_PASSWORD = my_config.get('DATABASE', 'password')

