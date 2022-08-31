import configparser
import os
from typing import Optional

from pydantic import BaseModel


class ServerConfig(BaseModel):
    log_dir: Optional[str]

    database_server: Optional[str]
    database_name: Optional[str]
    database_username: Optional[str]
    database_password: Optional[str]

    def __init__(self, config_file_path: str = "rowantree.config", *args, **kwargs):
        super().__init__(*args, **kwargs)
        config = configparser.ConfigParser()
        config.read(config_file_path)

        # Directory Options
        self.log_dir = config.get("DIRECTORY", "logs_dir")

        # Database Options
        self.database_server = config.get("DATABASE", "server")
        self.database_name = config.get("DATABASE", "database")
        self.database_username = config.get("DATABASE", "username")
        self.database_password = config.get("DATABASE", "password")

        if "LOGS_DIR" in os.environ:
            self.log_dir = os.environ["LOGS_DIR"]

        if "DATABASE_SERVER" in os.environ:
            self.database_server = os.environ["DATABASE_SERVER"]

        if "DATABASE_NAME" in os.environ:
            self.database_name = os.environ["DATABASE_NAME"]

        if "DATABASE_USERNAME" in os.environ:
            self.database_username = os.environ["DATABASE_USERNAME"]

        if "DATABASE_PASSWORD" in os.environ:
            self.database_password = os.environ["DATABASE_PASSWORD"]
