#!flask/bin/python

import errno
import logging
import os


import mysql.connector
from mysql.connector import pooling
from mysql.connector import errorcode

import socket, errno
import time
import random

import lib.docker_config as config
import lib.personality

# https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist
def make_sure_path_exists(path):
    try:
        if os.path.exists(path) is False:
            os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

# Setup logging.
make_sure_path_exists(config.LOGS_DIR)
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG,
    filemode='w',
    filename="%s/%s.therowantree.server.log" % (config.LOGS_DIR, os.uname()[1])
)

try:
    cnxpool = pooling.MySQLConnectionPool(pool_name = "servercnxpool",
                                      pool_size = 32,
                                      user=config.API_DATABASE_USERNAME, password=config.API_DATABASE_PASSWORD,
                                      host=config.API_DATABASE_SERVER,
                                      database=config.API_DATABASE_NAME)
except socket.error, e:
    logging.debug(e)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        logging.debug("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        logging.debug("Database does not exist")
    else:
        logging.debug(err)


if __name__ == '__main__':
    logging.debug('starting.')
    me = lib.personality.Personality(cnxpool)
    while True:
        sleep_internval = random.randint(1, 10)
        logging.debug('sleeping for (' + str(sleep_internval) + ')')
        time.sleep(sleep_internval)
        logging.debug('  waking..')
        me.contemplate()



