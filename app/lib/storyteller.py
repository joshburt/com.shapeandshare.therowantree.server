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
        'decrease': [
            ['a fire rampages through one of the huts, destroying it.  all residents in the hut perished in the fire.', 1, 10],
            ['a terrible plague is fast spreading through the village.  the nights are rent with screams.  the only hope is a quick death.', 1, 20],
            ['a sickness is spreading through the village.  only a few die.  the rest bury them.', 1, 10],
            ['some villagers are ill', 1, 3]
        ]
    }

    events = {
        'global': [
            {
                'title': 'A Beast Attack',
                'requirements': {
                    'population': 1
                },
                'text': [
                    'a pack of snarling beasts pours out of the trees.',
                    'the fight is short and bloody, but the beasts are repelled.',
                    'the villagers retreat to mourn the dead.'
                ],
                'notification': 'wild beasts attack the villagers',
                'reward': {
                    'fur': 100,
                    'meat': 100,
                    'teeth': 10
                },
                'boon': {
                    'population': 10
                }
            },
            {
                'title': 'A Robot Attack',
                'requirements': {
                    'population': 5
                },
                'text': [
                    'a dented and rattling robot rolls into view, sparks falling from lose wires as they arc against its frame.',
                    'a remnant from some ancient war.'
                ],
                'notification': 'a robot opens fire on the villagers',
                'reward': {
                    'gems': 1,
                    'coins': 10
                },
                'boon': {
                    'population': 1
                }
            },
            {
                'title': 'A Ghoul Attack',
                'requirements': {
                    'population': 15
                },
                'text': [
                    'the groans could be heard a few hours before they dragged themselves through the main part of the settlement',
                    'the awful smell, even worse those eyes',
                    'some of our own dead rose again, and had to be put to rest one final time.'
                ],
                'notification': 'a heard of ghouls wanders through the settlement',
                'reward': {
                    'gems': 1,
                    'coins': 10,
                    'fur': 100,
                    'meat': 10,
                    'teeth': 10
                },
                'boon': {
                    'population': 5
                }
            },
            {
                'title': 'The Forest Has Legs',
                'requirements': {
                    'population': 30
                },
                'text': [
                    'maybe it was their time to swarm, or just the presence of the settlement',
                    'the forest came alive as they blanketed everything, assaulting and cocooning all those who fell to them',
                    'moarn not those who died, but those the spiders took away'
                ],
                'notification': 'the skittering as the spiders retreated back into the forest haunts the dreams of even the bravest of those who survived',
                'reward': {
                    'gems': 1,
                    'coins': 10,
                    'fur': 100,
                    'meat': 10,
                    'teeth': 10
                },
                'boon': {
                    'population': 10
                }
            }
        ]
    }

    def __init__(self):
        logging.debug('lore master exists.')

    def populationIncreaseEvent(self):
        eventIndex = random.randint(1, len(self.population_events['increase'])) - 1
        eventDescription = self.population_events['increase'][eventIndex][0]
        eventMinAmount = self.population_events['increase'][eventIndex][1]
        eventMaxAmount = self.population_events['increase'][eventIndex][2]
        eventOutcome = random.randint(eventMinAmount, eventMaxAmount)
        return eventDescription, eventOutcome

    def populationDecreaseEvent(self):
        eventIndex = random.randint(1, len(self.population_events['decrease'])) - 1
        eventDescription = self.population_events['decrease'][eventIndex][0]
        eventMinAmount = self.population_events['decrease'][eventIndex][1]
        eventMaxAmount = self.population_events['decrease'][eventIndex][2]
        eventOutcome = random.randint(eventMinAmount, eventMaxAmount) * -1
        return eventDescription, eventOutcome

    def generateEvent(self, target_user):
        num_events = len(self.events['global'])
        event_index = random.randint(1, num_events) - 1
        new_event = self.events['global'][event_index]

        # check requirements
        requirement_check = True
        for requirement in new_event['requirements']:
            if requirement == 'population':
                min_required_pop = new_event['requirements'][requirement]
                logging.debug('required pop: ' + str(min_required_pop))

                #TODO: check the requirement
            else:
                logging.debug('required state: ' + requirement)

        if requirement_check is True:
            return new_event

        return None