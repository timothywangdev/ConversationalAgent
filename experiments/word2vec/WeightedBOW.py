from subreddit import SUBREDDITS
import sys
import numpy as np

WORD_VEC = dict()
DIM = 100
IDF = dict()
TOTAL_DOC = 54564441 - 364

if len(sys.argv) < 3:
    print "Usage: python bow.py [word_vector_file] [word_frequency_file]"
    sys.exit(1)

with open(sys.argv[1], 'rb') as input:
	print "Reading word vector representations."
	global WORD_VEC
        input.readline()
	for line in input:
		arr = line.split(' ')
                word = arr[0]
                vec = arr[1:]
		if len(vec) != DIM:
                        raise Exception("Vector for word: " + word + " has wrong dimension!")
		WORD_VEC[word] = np.array(vec).astype(np.float) 

with open(sys.argv[2], 'r') as input:
	print "Reading word document frequency."
	global IDF
	for line in input:
		arr = line.split(' ')
		IDF[arr[0]] = int(arr[1])

def generate_feature(subreddit_name):
	print "Generating feature vectors for " + subreddit_name
	input = open('./data/'+subreddit_name+'.sub')
	with open('./data/'+subreddit_name+'.fea', 'wb') as output:
		for comment in input:
			feature = np.zeros(DIM)
			words = filter(lambda x: x, comment.split(' '))
			word_count = dict()
			for word in words:
				if word in word_count:
					word_count[word] += 1
				else:
					word_count[word] = 1
			for word in words:
				if word in WORD_VEC and word in IDF:
					feature += ((1 + np.log(word_count[word])) * np.log(TOTAL_DOC / float(IDF[word])) * WORD_VEC[word])
			output.write(feature)
			output.write('\n')

for sub in SUBREDDITS:
	generate_feature(sub)
