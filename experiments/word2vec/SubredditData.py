from DataGenerator import *

LEFT_PARTY = ['liberal', 'alltheleft']
RIGHT_PARTY = ['new_right', 'conservative', 'republicans']
LEFT_RIGHT_DICT = dict()
for sub in LEFT_PARTY:
    LEFT_RIGHT_DICT[sub] = 'leftparty'
for sub in RIGHT_PARTY:
    LEFT_RIGHT_DICT[sub] = 'rightparty'

do('./data/data.json', subreddit=LEFT_RIGHT_DICT)
