import logging
import errno
import socket
import mysql.connector
from mysql.connector import pooling
from mysql.connector import errorcode
import random
import time
import json

import storyteller

class Personality:

    MAX_NAPPY_TIME = 3 # in seconds
    ENCOUNTER_CHANGE = 100 # in percent

    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.loremaster = storyteller.StoryTeller()

    def contemplate(self):
        # get active users
        user_set = self.get_active_users()
        for target_user in user_set:

            # Lets add an encounter
            self.encounter(target_user)

        # now sleep..
        self.slumber()

    def encounter(self, target_user):
        if self.luck(self.ENCOUNTER_CHANGE) is True:
            user_stores = self.get_user_stores(target_user)
            event = self.loremaster.generateEvent(self.get_user_population(target_user), user_stores)
            self.process_user_event(event, target_user)

    def slumber(self):
        sleep_internval = random.randint(1, self.MAX_NAPPY_TIME)
        # logging.debug('sleeping for (' + str(sleep_internval) + ')')
        time.sleep(sleep_internval)
        # logging.debug('  waking..')

    ##############
    ## Data Tier
    ##############
    def get_active_users(self):
        my_active_users = []
        rows = self.callProc('getActiveUsers', [])
        for tuple in rows:
            my_active_users.append(tuple[0])
        return my_active_users

    def get_user_population(self, target_user):
        user_population = None
        rows = self.callProc('getUserPopulationByID', [target_user,])
        for tuple in rows:
            user_population = tuple[0]
        return user_population

    def get_user_stores(self, target_user):
        user_stores = {}
        rows = self.callProc('getUserStoresByID', [target_user,])
        for tuple in rows:
            user_stores[tuple[0]] = tuple[2]
        return user_stores

    def luck(self, odds):
        ## Ask only for what you truely need and beware
        ## you may be granted your wish.
        flip = random.randint(1, 100)
        if flip <= odds:
            return True
        return False

    ##############
    ## Event Queueing
    ##############
    def process_action_queue(self, action_queue):
        # logging.debug(action_queue)
        for action in action_queue:
            self.callProc(action[0], action[1])

    def process_user_event(self, event, target_user):
        if event is None:
            return

        action_queue = []
        user_stores = self.get_user_stores(target_user)

        # process rewards
        if 'reward' in event:
            for reward in event['reward']:
                amount = random.randint(1, event['reward'][reward])

                if reward == 'population':
                    action_queue.append(['deltaUserPopulationByID', [target_user, amount]])
                    event['reward'][reward] = amount
                else:
                    if reward in user_stores:
                        store_amt = user_stores[reward]
                        if store_amt < amount:
                            amount = store_amt
                        action_queue.append(['deltaUserStoreByStoreName', [target_user, reward, amount]])
                        event['reward'][reward] = amount

        # process curses
        if 'curse' in event:
            for curse in event['curse']:
                if curse == 'population':
                    pop_amount = random.randint(1, event['curse'][curse])
                    if self.get_user_population(target_user) < pop_amount:
                        pop_amount = self.get_user_population(target_user)
                    action_queue.append(['deltaUserPopulationByID', [target_user, (pop_amount * -1)]])
                    event['curse'][curse] = pop_amount
                else:
                    amount = random.randint(1, event['curse'][curse])
                    if curse in user_stores:
                        store_amt = user_stores[curse]
                        if store_amt < amount:
                            amount = store_amt
                    action_queue.append(['deltaUserStoreByStoreName', [target_user, curse, (amount * -1)]])
                    event['curse'][curse] = amount

        # Send them the whole event object.
        action_queue.append(['sendUserNotification', [target_user, json.dumps(event)]])

        self.process_action_queue(action_queue)

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
