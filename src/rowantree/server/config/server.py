import configparser
import os


class ServerConfig:
    log_dir: str
    tmp_dir: str

    api_access_key: str
    api_version: str
    listening_host: str
    flask_debug: bool

    api_database_server: str
    api_database_name: str
    api_database_username: str
    api_database_password: str

    def __init__(self, config_file_path: str = "rowantree.config"):
        config = configparser.ConfigParser()
        config.read(config_file_path)

        # Directory Options
        self.log_dir = config.get("DIRECTORY", "logs_dir")
        self.tmp_dir = config.get("DIRECTORY", "tmp_dir")

        # Server Options
        self.api_access_key = config.get("SERVER", "api_access_key")
        self.api_version = config.get("SERVER", "api_version")
        self.listening_host = config.get("SERVER", "listening_host")
        self.flask_debug = config.getboolean("SERVER", "flask_debug")

        # Database Options
        self.api_database_server = config.get("DATABASE", "server")
        self.api_database_name = config.get("DATABASE", "database")
        self.api_database_username = config.get("DATABASE", "username")
        self.api_database_password = config.get("DATABASE", "password")

        if "LOGS_DIR" in os.environ:
            self.log_dir = os.environ["LOGS_DIR"]

        if "TMP_DIR" in os.environ:
            self.tmp_dir = os.environ["TMP_DIR"]

        if "API_ACCESS_KEY" in os.environ:
            self.api_access_key = os.environ["API_ACCESS_KEY"]

        if "API_VERSION" in os.environ:
            self.api_version = os.environ["API_VERSION"]

        if "LISTENING_HOST" in os.environ:
            self.listening_host = os.environ["LISTENING_HOST"]

        if "FLASK_DEBUG" in os.environ:
            self.flask_debug = bool(os.environ["FLASK_DEBUG"])

        if "API_DATABASE_SERVER" in os.environ:
            self.api_database_server = os.environ["API_DATABASE_SERVER"]

        if "API_DATABASE_NAME" in os.environ:
            self.api_database_name = os.environ["API_DATABASE_NAME"]

        if "API_DATABASE_USERNAME" in os.environ:
            self.api_database_username = os.environ["API_DATABASE_USERNAME"]

        if "API_DATABASE_PASSWORD" in os.environ:
            self.api_database_password = os.environ["API_DATABASE_PASSWORD"]
