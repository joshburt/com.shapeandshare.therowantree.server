""" Database DAO Definition """

import logging
import socket
from typing import Any, Tuple

import mysql.connector
from mysql.connector import errorcode
from mysql.connector.pooling import MySQLConnectionPool


class DBDAO:
    """
    Database DAO

    Attributes
    ----------
    cnxpool: Any
        MySQL Connection Pool
    """

    cnxpool: MySQLConnectionPool

    def __init__(self, cnxpool: MySQLConnectionPool):
        self.cnxpool = cnxpool

    def get_active_users(self) -> list[str]:
        my_active_users: list[str] = []
        rows: list[Tuple] = self._call_proc("getActiveUsers", [])
        for response_tuple in rows:
            my_active_users.append(response_tuple[0])
        return my_active_users

    def get_user_population(self, target_user) -> int:
        rows: list[Tuple] = self._call_proc(
            "getUserPopulationByID",
            [
                target_user,
            ],
        )
        return rows[0][0]

    def get_user_stores(self, target_user) -> dict[str, Any]:
        user_stores: dict[str, Any] = {}
        rows: list[Tuple] = self._call_proc(
            "getUserStoresByID",
            [
                target_user,
            ],
        )
        for response_tuple in rows:
            user_stores[response_tuple[0]] = response_tuple[2]
        return user_stores

    def process_action_queue(self, action_queue) -> None:
        # logging.debug(action_queue)
        for action in action_queue:
            self._call_proc(action[0], action[1])

    def _call_proc(self, name, args) -> list[Tuple]:
        rows: list[Tuple] = []
        try:
            cnx = self.cnxpool.get_connection()
            cursor = cnx.cursor()
            cursor.callproc(name, args)
            for result in cursor.stored_results():
                rows = result.fetchall()
            cursor.close()
        except socket.error as e:
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

        if rows is None:
            raise "Failure getting database information"

        return rows
