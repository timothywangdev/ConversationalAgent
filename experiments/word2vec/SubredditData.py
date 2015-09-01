from DataGenerator import *

do('./data/data.json', './data/leftwing', 
        subreddit=['liberal', 'alltheleft'])

do('./data/data.json', './data/rightwing', 
        subreddit=['new_right', 'conservative', 'republicans'])
