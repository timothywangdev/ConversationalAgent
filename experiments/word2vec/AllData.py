from DataGenerator import *
import os

if os.path.exists(FOUT_PATH):
    os.remove(FOUT_PATH)

do('./data/RC_2015-03.json')
