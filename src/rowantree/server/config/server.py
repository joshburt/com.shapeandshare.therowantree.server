""" Server Config Definition """

import configparser
import os
from typing import Any, Optional

from pydantic import BaseModel


class ServerConfig(BaseModel):
    """
    Server Configuration

    Attributes
    ----------
    config_file_path: Optional[str] = "rowantree.config"
        The config file for the service.
    log_dir: Optional[str]
        The log directory.
    """

    config_file_path: Optional[str] = "rowantree.config"
    log_dir: Optional[str]

    def __init__(self, **data: Any):
        super().__init__(**data)
        config = configparser.ConfigParser()
        config.read(self.config_file_path)

        # Directory Options
        self.log_dir = config.get("DIRECTORY", "logs_dir")

        if "LOGS_DIR" in os.environ:
            self.log_dir = os.environ["LOGS_DIR"]
