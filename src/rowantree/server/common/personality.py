import json
import random
import time
from typing import Any, Optional

from rowantree.contracts import Action, ActionQueue, UserPopulation, UserStore, UserStores, WorldStatus
from rowantree.service.sdk import RowanTreeService

from .storyteller import StoryTeller


class Personality:
    rowantree_service: RowanTreeService
    loremaster: StoryTeller

    max_sleep_time: int  # in seconds
    encounter_change: int  # in percent

    def __init__(self, rowantree_service: RowanTreeService, max_sleep_time: int = 3, encounter_change: int = 100):
        self.rowantree_service = rowantree_service
        self.max_sleep_time = max_sleep_time
        self.encounter_change = encounter_change
        self.loremaster = StoryTeller()

    def contemplate(self) -> None:
        # get active users
        world_status: WorldStatus = self.rowantree_service.world_status_get()
        for target_user in world_status.active_players:
            # Lets add an encounter
            self._encounter(target_user=target_user)

        # now sleep..
        self._slumber()

    def _encounter(self, target_user: str) -> None:
        if Personality._luck(odds=self.encounter_change) is True:
            user_stores: UserStores = self.rowantree_service.user_stores_get(user_guid=target_user)
            user_population: UserPopulation = self.rowantree_service.user_population_get(user_guid=target_user)

            event: Optional[dict] = self.loremaster.generate_event(
                user_population=user_population, user_stores=user_stores
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

    # TODO: Review the complexity of this
    # pylint: disable=too-many-branches
    def _process_user_event(self, event: Optional[Any], target_user: str) -> None:
        if event is None:
            return

        action_queue: ActionQueue = ActionQueue(queue=[])
        user_stores: UserStores = self.rowantree_service.user_stores_get(user_guid=target_user)

        # convert to dictionary
        user_stores_dict: dict[str, UserStore] = {}
        for store in user_stores.stores:
            user_stores_dict[store.name] = store

        # process rewards
        if "reward" in event:
            for reward in event["reward"]:
                amount: int = random.randint(1, event["reward"][reward])

                if reward == "population":
                    action_queue.queue.append(Action(name="deltaUserPopulationByID", arguments=[target_user, amount]))
                    event["reward"][reward] = amount
                else:
                    if reward in user_stores_dict:
                        store_amt = user_stores_dict[reward].amount
                        if store_amt < amount:
                            amount = store_amt

                        action_queue.queue.append(
                            Action(name="deltaUserStoreByStoreName", arguments=[target_user, reward, amount])
                        )
                        event["reward"][reward] = amount

        # process curses
        if "curse" in event:
            for curse in event["curse"]:
                if curse == "population":
                    pop_amount: int = random.randint(1, event["curse"][curse])
                    user_population: UserPopulation = self.rowantree_service.user_population_get(user_guid=target_user)
                    if user_population.population < pop_amount:
                        pop_amount: int = user_population.population

                    action_queue.queue.append(
                        Action(name="deltaUserPopulationByID", arguments=[target_user, (pop_amount * -1)])
                    )
                    event["curse"][curse] = pop_amount
                else:
                    amount: int = random.randint(1, event["curse"][curse])
                    if curse in user_stores:
                        store_amt = user_stores_dict[curse].amount
                        if store_amt < amount:
                            amount = store_amt

                    action_queue.queue.append(
                        Action(name="deltaUserStoreByStoreName", arguments=[target_user, curse, (amount * -1)])
                    )
                    event["curse"][curse] = amount

        # Send them the whole event object.
        action_queue.queue.append(Action(name="sendUserNotification", arguments=[target_user, json.dumps(event)]))

        self.rowantree_service.action_queue_process(queue=action_queue)
