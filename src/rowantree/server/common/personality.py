import json
import random
import time
from typing import Any, Optional

from .db_dao import DBDAO
from .storyteller import StoryTeller


class Personality:
    dao: DBDAO
    loremaster: StoryTeller

    max_sleep_time: int  # in seconds
    encounter_change: int  # in percent

    def __init__(self, dao: DBDAO, max_sleep_time: int = 3, encounter_change: int = 100):
        self.dao = dao
        self.max_sleep_time = max_sleep_time
        self.encounter_change = encounter_change
        self.loremaster = StoryTeller()

    def contemplate(self) -> None:
        # get active users
        user_set: list[str] = self.dao.get_active_users()

        for target_user in user_set:
            # Lets add an encounter
            self._encounter(target_user=target_user)

        # now sleep..
        self._slumber()

    def _encounter(self, target_user: str) -> None:
        if Personality._luck(odds=self.encounter_change) is True:
            user_stores: dict[str, Any] = self.dao.get_user_stores(target_user)
            event: Optional[Any] = self.loremaster.generate_event(
                self.dao.get_user_population(target_user), user_stores
            )
            self._process_user_event(event=event, target_user=target_user)

    def _slumber(self):
        time.sleep(random.randint(1, self.max_sleep_time))

    @staticmethod
    def _luck(odds) -> bool:
        # Ask only for what you truely need and beware you may be granted your wish.
        flip: int = random.randint(1, 100)
        if flip <= odds:
            return True
        return False

    ##############
    ## Event Queueing
    ##############

    def _process_user_event(self, event: Optional[Any], target_user: str) -> None:
        if event is None:
            return

        action_queue = []
        user_stores: dict[str, Any] = self.dao.get_user_stores(target_user)

        # process rewards
        if "reward" in event:
            for reward in event["reward"]:
                amount: int = random.randint(1, event["reward"][reward])

                if reward == "population":
                    action_queue.append(["deltaUserPopulationByID", [target_user, amount]])
                    event["reward"][reward] = amount
                else:
                    if reward in user_stores:
                        store_amt = user_stores[reward]
                        if store_amt < amount:
                            amount = store_amt
                        action_queue.append(["deltaUserStoreByStoreName", [target_user, reward, amount]])
                        event["reward"][reward] = amount

        # process curses
        if "curse" in event:
            for curse in event["curse"]:
                if curse == "population":
                    pop_amount: int = random.randint(1, event["curse"][curse])
                    if self.dao.get_user_population(target_user) < pop_amount:
                        pop_amount: int = self.dao.get_user_population(target_user)
                    action_queue.append(["deltaUserPopulationByID", [target_user, (pop_amount * -1)]])
                    event["curse"][curse] = pop_amount
                else:
                    amount: int = random.randint(1, event["curse"][curse])
                    if curse in user_stores:
                        store_amt = user_stores[curse]
                        if store_amt < amount:
                            amount = store_amt
                    action_queue.append(["deltaUserStoreByStoreName", [target_user, curse, (amount * -1)]])
                    event["curse"][curse] = amount

        # Send them the whole event object.
        action_queue.append(["sendUserNotification", [target_user, json.dumps(event)]])

        self.dao.process_action_queue(action_queue)
