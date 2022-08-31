import logging
import os
import socket
from pathlib import Path

import mysql.connector
from mysql.connector import errorcode, pooling

from .common.db_dao import DBDAO
from .common.personality import Personality
from .config.server import ServerConfig

if __name__ == "__main__":
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

    try:
        logging.debug("Connecting to database")
        cnxpool = pooling.MySQLConnectionPool(
            pool_name="servercnxpool",
            pool_size=32,
            user=config.api_database_username,
            password=config.api_database_password,
            host=config.api_database_server,
            database=config.api_database_name,
        )

        logging.debug("Creating personality")
        me = Personality(dao=DBDAO(cnxpool=cnxpool))
        logging.debug("Starting contemplation loop")
        while True:
            me.contemplate()
    except socket.error as error:
        logging.debug(error)
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.debug("Something is wrong with your user name or password")
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            logging.debug("Database does not exist")
        else:
            logging.debug(error)
