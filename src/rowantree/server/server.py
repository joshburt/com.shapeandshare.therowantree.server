""" Content Service Entry Point """

import logging
import os
from pathlib import Path

from rowantree.service.sdk import RowanTreeService

from .common.personality import Personality
from .config.server import ServerConfig

if __name__ == "__main__":
    # Generating server configuration
    config: ServerConfig = ServerConfig()

    # Setup logging
    Path(config.log_dir).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.DEBUG,
        filemode="w",
        filename=f"{config.log_dir}/{os.uname()[1]}.therowantree.server.log",
    )

    logging.debug("Starting server")

    logging.debug(config.json(by_alias=True, exclude_unset=True))

    me: Personality = Personality(rowantree_service=RowanTreeService())

    logging.debug("Starting contemplation loop")
    while True:
        me.contemplate()
