import logging
import random

class StoryTeller:

    MAX_ENCOUNTER_TRIES = 10

    events = {
        'global': [
            {
                'title': 'a stranger arrives in the night',
                'requirements': {
                    'population': 0
                },
                'reward': {
                    'population': 1
                }
            },
            {
                'title': 'a weathered family takes up in one of the huts',
                'requirements': {
                    'population': 1
                },
                'reward': {
                    'population': 3
                }
            },
            {
                'title': 'a small group arrives, all dust and bones',
                'requirements': {
                    'population': 1
                },
                'reward': {
                    'population': 5
                }
            },
            {
                'title': 'a convoy lurches in, equal parts worry and hope',
                'requirements': {
                    'population': 1
                },
                'reward': {
                    'population': 6
                }
            },
            {
                'title': 'a half-feral and malnourished child is discovered huddled by the great tree',
                'requirements': {
                    'population': 1
                },
                'reward': {
                    'population': 1
                }
            },
            {
                'title': 'another lone wanderer comes into town, in tears to have found a place of sanctuary against the world',
                'requirements': {
                    'population': 1
                },
                'reward': {
                    'population': 1
                }
            },
            {
                'title': 'a fire rampages through one of the huts, destroying it.',
                'requirements': {
                    'population': 15
                },
                'text': [
                    'all residents in the hut perished in the fire.'
                ],
                'boon': {
                    'population': 10
                }
            },
            {
                'title': 'a terrible plague is fast spreading through the village.',
                'requirements': {
                    'population': 20
                },
                'text': [
                    'the nights are rent with screams.',
                    'the only hope is a quick death.'
                ],
                'boon': {
                    'population': 15
                }
            },
            {
                'title': 'a sickness is spreading through the village.',
                'requirements': {
                    'population': 15
                },
                'text': [
                    'only a few die.',
                    'the rest bury them.'
                ],
                'boon': {
                    'population': 10
                }
            },
            {
                'title': 'some villagers are ill',
                'requirements': {
                    'population': 6
                },
                'boon': {
                    'population': 3
                }
            },
            {
                'title': 'A Beast Attack',
                'requirements': {
                    'population': 15
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
                    'population': 10
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
                    'population': 20
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

    def generateEvent(self, user_population):
        num_events = len(self.events['global'])
        requirement_check = False
        counter = 0
        new_event = None

        while requirement_check is False:
            counter += 1
            event_index = random.randint(1, num_events) - 1
            new_event = self.events['global'][event_index]

            # check requirements
            for requirement in new_event['requirements']:
                if requirement == 'population':
                    min_required_pop = new_event['requirements'][requirement]
                    logging.debug('reported user population: ' + str(user_population))
                    if user_population >= min_required_pop:
                        requirement_check = True

            # bail out if we've reached out max, i guess they get a boring time..
            if counter >= self.MAX_ENCOUNTER_TRIES:
                new_event = None
                requirement_check = True

        return new_event