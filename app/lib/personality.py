import logging
import errno
import socket
import mysql.connector
from mysql.connector import pooling
from mysql.connector import errorcode

class Personality:

    def __init__(self, cnxpool):
        self.cnxpool = cnxpool

    def contemplate(self):
        # get active users
        logging.debug('  contemplating..')
        user_set = self.get_active_users()

    def get_active_users(self):
        try:
            cnx = self.cnxpool.get_connection()
            cursor = cnx.cursor()
            args = []
            results = cursor.callproc('', args)
            cursor.close()
        except socket.error, e:
            logging.debug(e)
        except mysql.connector.Error as err:
         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.debug("Something is wrong with your user name or password")
         elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logging.debug("Database does not exist")
         else:
            logging.debug(err)
        else:
            cnx.close()

