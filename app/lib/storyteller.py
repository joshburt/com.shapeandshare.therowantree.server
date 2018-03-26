import logging

class StoryTeller:
    def __init__(self):
        logging.debug('lore master exists.')

    def populationIncreaseEvent(self):
        eventDescription = 'population increased'
        eventOutcome = 1
        return eventDescription, eventOutcome

    def populationDecreaseEvent(self):
        eventDescription = 'population descreased'
        eventOutcome = -1
        return eventDescription, eventOutcome
