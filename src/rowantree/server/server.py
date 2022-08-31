import logging
import os
from pathlib import Path

from mysql.connector.pooling import MySQLConnectionPool

from .common.personality import Personality
from .config.server import ServerConfig
from .db.dao import DBDAO
from .db.utils import get_connect_pool

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
        filename="%s/%s.therowantree.server.log" % (config.log_dir, os.uname()[1]),
    )

    logging.debug("Starting server")

    logging.debug(config.json(by_alias=True, exclude_unset=True))

    # Creating database connection pool
    cnxpool: MySQLConnectionPool = get_connect_pool(config=config)

    me: Personality = Personality(dao=DBDAO(cnxpool=cnxpool))

    logging.debug("Starting contemplation loop")
    while True:
        me.contemplate()
