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
        user_set = self.get_active_users()
        for target_user in user_set:

            # Lets add an encounter
            self.encounter(target_user)

            # Review for population changes
            self.population_review(target_user)

        # now sleep..
        self.slumber()

    def population_review(self, target_user):
        # Review for population changes
        amount, notification = None, None
        if self.luck(10) is True:
            if self.luck(50) is True:
                # lets schedule a population increase
                notification, amount = self.loremaster.populationIncreaseEvent()
            else:
                # lets schedule a population decrease
                notification, amount = self.loremaster.populationDecreaseEvent()

            action_queue = [
                ['deltaUserPopulationByID', [target_user, amount]],
                ['sendUserNotification', [target_user, notification]]
            ]
            self.process_action_queue(action_queue)

    def encounter(self, target_user):
        if self.luck(10) is True:
            event = self.loremaster.generateEvent(self.get_user_population(target_user))
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

        # add the event title
        action_queue.append(['sendUserNotification', [target_user, event['title']]])

        # process and add event text
        for line in event['text']:
            action_queue.append(['sendUserNotification', [target_user, line]])

        # add event notification
        action_queue.append(['sendUserNotification', [target_user, event['notification']]])

        # process rewards
        for reward in event['reward']:
            amount = random.randint(1, event['reward'][reward])
            # logging.debug('should process reward ' + reward + ': ' + str(amount))
            action_queue.append(['sendUserNotification', [target_user, 'reward increased by ' + str(amount)]])
            action_queue.append(['deltaUserStoreByStoreName',[target_user, reward, amount]])

        # process boons
        for boon in event['boon']:
            amount = random.randint(1, event['boon'][boon]) * -1
            if boon == 'population':
                action_queue.append(['sendUserNotification', [target_user, 'population decreased by ' + str(amount)]])
                action_queue.append(['deltaUserPopulationByID', [target_user, amount]])

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
