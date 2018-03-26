import logging
import errno
import socket
import mysql.connector
from mysql.connector import pooling
from mysql.connector import errorcode
import random
import time

import storyteller

class Personality:

    MAX_NAPPY_TIME = 10 # in seconds


    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.loremaster = storyteller.StoryTeller()

    def contemplate(self):
        # get active users
        # logging.debug('  contemplating..')
        user_set = self.get_active_users()
        for target_user in user_set:
            # logging.debug('    processing user (' + str(target_user) + ')')

            # Review for population changes
            self.populationReview(target_user)

        # now sleep..
        self.slumber()

    def slumber(self):
        sleep_internval = random.randint(1, self.MAX_NAPPY_TIME)
        # logging.debug('sleeping for (' + str(sleep_internval) + ')')
        time.sleep(sleep_internval)
        # logging.debug('  waking..')

    def populationReview(self, target_user):
        # Review for population changes
        amount, notification = None, None
        if self.luck(10) is True:
            if self.luck(50) is True:
                # logging.debug('     its your day!')
                # lets schedule a population increase
                # and send off a notification
                notification, amount = self.loremaster.populationIncreaseEvent()
            else:
                # logging.debug('      uh ho..')
                # lets schedule a population descrease
                # and send off a notification
                notification, amount = self.loremaster.populationDecreaseEvent()

            self.callProc('deltaUserPopulationByID', [target_user, amount])
            self.callProc('sendUserNotification', [target_user, notification])

    ##############
    ## Data Tier
    ##############

    def callProc(self, name, args):
        rows = None
        try:
            cnx = self.cnxpool.get_connection()
            cursor = cnx.cursor()
            cursor.callproc(name, args)
            for result in cursor.stored_results():
                rows = result.fetchall()
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
        return rows

    def get_active_users(self):
        my_active_users = []
        rows = self.callProc('getActiveUsers', [])
        for tuple in rows:
            my_active_users.append(tuple[0])
        return my_active_users

    def luck(self, odds):
        ## Ask only for what you truely need and beware
        ## you may be granted your wish.
        flip = random.randint(1, 100)
        if flip <= odds:
            return True
        return False
