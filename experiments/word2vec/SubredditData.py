from DataGenerator import *
import os

SUBREDDITS = ['liberal', 'alltheleft', 'new_right', 'conservative', 'republicans']

for sub in SUBREDDITS:
    sub_file = './data/'+sub+'.sub'
    sub_author_file = './data/'+sub+'.aut'
    if os.path.exists(sub_file):
        os.remove(sub_file)
    if os.path.exists(sub_author_file):
        os.remove(sub_author_file)

do('./data/RC_2015-03.json', subreddit=SUBREDDITS)
