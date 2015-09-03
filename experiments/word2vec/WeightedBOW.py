from subreddit import SUBREDDITS
import sys
import numpy as np

DIM = 100
TOTAL_DOC = 54564441 - 364

if len(sys.argv) < 3:
    print "Usage: python bow.py [word_vector_file] [word_frequency_file]"
    sys.exit(1)

def read_word_vec(infile):
    with open(infile, 'rb') as input:
	print "Reading word vector representations."
	WORD_VEC = dict()
        input.readline()
	for line in input:
            arr = line.split(' ')
            word = arr[0]
            vec = arr[1:]
            if len(vec) != DIM:
                raise Exception("Vector for word: " + word + " has wrong dimension!")
            WORD_VEC[word] = np.array(vec).astype(np.float) 
        return WORD_VEC

def read_word_freq(infile):
    with open(infile, 'r') as input:
	print "Reading word document frequencies."
	IDF = dict()
	for line in input:
            arr = line.split(' ')
            IDF[arr[0]] = int(arr[1])
        return IDF

def generate_feature(subreddit_name, vec_dict, freq_dict):
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
                    if word in vec_dict and word in freq_dict:
                        feature += ((1 + np.log(word_count[word])) * np.log(TOTAL_DOC / float(freq_dict[word])) * vec_dict[word])
                output.write(feature)
                output.write('\n')

vectors = read_word_vec(sys.argv[1])
freqs = read_word_freq(sys.argv[2])
for sub in SUBREDDITS:
    generate_feature(sub, vectors, freqs)

