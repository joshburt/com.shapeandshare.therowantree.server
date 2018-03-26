import logging
import random

class StoryTeller:

    # DESCRIPTION, MIN AMOUNT, MAX AMOUNT
    population_events = {
        'increase': [
            ['a stranger arrives in the night', 1, 1],
            ['a weathered family takes up in one of the huts', 2, 3],
            ['a small group arrives, all dust and bones', 4, 6],
            ['a convoy lurches in, equal parts worry and hope', 4, 8],
            ['a half-feral and malnourished child is discovered huddled by the great tree', 1, 1],
            ['another lone wanderer comes into town, in tears to have found a place of sanctuary against the world', 1, 1]
        ],
        'descrease': {}
    }

    def __init__(self):
        logging.debug('lore master exists.')

    def populationIncreaseEvent(self):
        # eventDescription = 'population increased'
        # eventOutcome = 1

        eventIndex = random.randint(1, len(self.population_events['increase'])) - 1
        eventDescription = self.population_events['increase'][eventIndex][0]
        eventMinAmount = self.population_events['increase'][eventIndex][1]
        eventMaxAmount = self.population_events['increase'][eventIndex][2]
        eventOutcome = random.randint(eventMinAmount, eventMaxAmount)

        return eventDescription, eventOutcome

    def populationDecreaseEvent(self):
        eventDescription = 'population descreased'
        eventOutcome = -1
        return eventDescription, eventOutcome
