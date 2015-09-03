__author__ = 'Hujie Wang'

import json
import re
import keras as T
import time
import os, sys
import codecs

FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)
FOUT_PATH="./data/data_generated"
SELECTED_SUBREDDIT=[]
number_of_tokens=0
number_of_comments=0
last_number_of_comments=0
start_time=None
comment_dict = dict()

'''
class ConcatJSONDecoder(json.JSONDecoder):
    def decode(self, s, _w=WHITESPACE.match):
        s_len = len(s)

        objs = []
        end = 0
        while end != s_len:
            obj, end = self.raw_decode(s, idx=_w(s, end).end())
            end = _w(s, end).end()
            generate(obj)
        return None
'''

def do(fname, subreddit=[]):
	'''
	:param fname(Reddit comment JSON file)
	:      subreddit(a list of subreddit names)
	:return a dict of JSON object:
	'''
	global start_time
	global number_of_tokens
	global number_of_comments
	global last_number_of_comments
	global FOUT_PATH
	global SELECTED_SUBREDDIT
	start_time = time.time()
	number_of_tokens=0
	number_of_comments=0
	last_number_of_comments=0
	SELECTED_SUBREDDIT=subreddit
	print('Converting reddit comments into tokens...')
	with open(fname) as data_file:
		line = data_file.readline()
		while line:
			generate(json.loads(line))
			line = data_file.readline()
	if subreddit:
		global comment_dict
		with open('./data/word_idf', 'wb') as out:
			for key, value in comment_dict.iteritems():
				out.write(key + ' ' + str(value) + '\n')
	print('Data generation completed!')
	print('Number of comments:'+str(number_of_comments))
	print('Number of tokens:'+str(number_of_tokens))

def getString(obj):
        '''
        Return a list of strings given a JSON data

        :param data (JSON)
        :return: a list of strings
        '''
        global start_time
        global last_number_of_comments
        current_time=time.time()
        #duration=int((current_time - start_time)*1000)
        return obj['body'].encode('utf8')

def string2sentences(str):
        '''
        :param str:
        :return a list of sentences:
        '''
        return list(filter(bool,re.split(r'[;,.!?]+',str)))


def write_comment(fname,sequences):
        '''
        Append list of tokens into a file(in binary), according to the data format of word2vec
        :param fname:
        :param l (list of strings):
        '''
        with open(fname,'ab') as fout:
            for i in range(len(sequences)):
                #for j in range(len(sequences[i])):
                #fout.write(bytes(sequences[i], 'UTF-8'))
                fout.write(bytes(sequences[i]))
                if i!=len(sequences)-1:
                    #fout.write(bytes(' ', 'UTF-8'))
                    fout.write(bytes(' '))
                else:
                    #fout.write(bytes('\n', 'UTF-8'))
                    fout.write(bytes('\n'))

def write(fname,sequences):
        '''
        Append list of tokens into a file(in binary), according to the data format of word2vec
        :param fname:
        :param l (list of strings):
        '''
        with codecs.open(fname,'ab') as fout:
            for i in range(len(sequences)):
                if len(sequences[i])==0:
                    continue
                for j in range(len(sequences[i])):
                    fout.write(sequences[i][j])
                    if j!=len(sequences[i])-1:
                        fout.write(u' ')
                    else:
                        fout.write(u'\n')

def text2sequence(text):
        '''
        Convert a string into a list of words, filtering punctuations and irreverent symbols
        :param text(a sttring):
        :return a list of words:
        '''
        global number_of_tokens
        sequence = T.text_to_word_sequence(text, filters=T.base_filter(), lower=True, split=" ")
        for i in range(len(sequence)):
            sequence[i]=re.sub(r'^[0-9]+$','<NUMBER>',sequence[i])
            number_of_tokens+=1
        return sequence

def generate(obj):
	global number_of_comments
	number_of_comments+=1
	if number_of_comments%100000==0:
		print(number_of_comments)
		#print(repr((number_of_comments-last_number_of_comments)/duration )+" comments per second" )
		#last_number_of_comments=number_of_comments

	#if obj['subreddit'] in SELECTED_SUBREDDIT or not SELECTED_SUBREDDIT:
	sequences=[]
	seq = []
	global number_of_tokens
	number_of_tokens+=1
	sentences=string2sentences(getString(obj))
	'''
	space = " "
	sentences=space.join(string2sentences(getString(obj)))
	sequences = text2sequence(sentences)
	sentences=string2sentences(getString(obj))
	'''
	for sentence in sentences:
		sequences.append(text2sequence(sentence))
		seq += sequences[-1]
	#if not SELECTED_SUBREDDIT:
	write(FOUT_PATH, sequences)
	#else:
	if obj['subreddit'] in SELECTED_SUBREDDIT:
		distinct = set(seq)
		global comment_dict
		for word in distinct:
			if word in comment_dict:
				comment_dict[word] += 1
			else:
				comment_dict[word] = 1
		party = obj['subreddit']
		write_comment('./data/'+party+'.sub', seq)
		with open('./data/'+party+'.aut', 'ab') as author:
			author.write(obj['author'])
			author.write('\n')

