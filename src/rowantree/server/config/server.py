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

    def __init__(self, *args, config_file_path: str = "rowantree.config", **kwargs):
        super().__init__(*args, **kwargs)
        config = configparser.ConfigParser()
        config.read(config_file_path)

        # Directory Options
        self.log_dir = config.get("DIRECTORY", "logs_dir")

        if "LOGS_DIR" in os.environ:
            self.log_dir = os.environ["LOGS_DIR"]
