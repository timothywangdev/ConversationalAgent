__author__ = 'Hujie Wang'

import json
import re
import time
import string
import codecs
import os, sys

from progressbar import Bar, ETA, Percentage, ProgressBar, RotatingMarker

FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)
FOUT_PATH="./data/data_generated"
SELECTED_SUBREDDIT=[]
number_of_tokens=0
number_of_comments=0
last_number_of_comments=0
start_time=None
IDF_DICT = dict()

def do(fname, subreddit=[], min_score=float('-inf'), min_length=0):
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
        global comment_dict
        start_time = time.time()
        number_of_tokens=0
        number_of_comments=0
        last_number_of_comments=0
        SELECTED_SUBREDDIT=subreddit
        print('Converting reddit comments into tokens...')

        widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
               ' ', ETA()]

        '''
        maxval: number of json objects(lines) in a file (Each line is a json object)

        data.json  (272  MB, time: 00:02:30): maxval=468317
        RC_2015-03 (32.6 GB, time: 02:32:34): maxval=54564441
        '''

        pbar = ProgressBar(widgets=widgets, maxval=54564441).start()
        nline=0
        with open(fname) as data_file:
            for line in data_file:
                obj = json.loads(line)
                generate(obj, min_score, min_length)
                pbar.update(nline+1)
                nline+=1
        pbar.finish()

        if subreddit:
            with codecs.open('./data/word_idf', 'wb', 'utf-8') as out:
                for key, value in IDF_DICT.iteritems():
                    out.write(key + ' ' + str(value) + '\n')

        print('\n')
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
        return obj['body']

def string2sentences(str):
        '''
        :param str:
        :return a list of sentences:
        '''
        return list(filter(bool,re.split(r'[;,.!?]+',str)))


def write(fname,sequences):
        '''
        Append list of tokens into a file(in binary), according to the data format of word2vec
        :param fname:
        :param l (list of strings):
        '''
        with codecs.open(fname,'ab','utf-8') as fout:
            for i in range(len(sequences)):
                if len(sequences[i])==0:
                    continue
                for j in range(len(sequences[i])):
                    fout.write(sequences[i][j])
                    if j!=len(sequences[i])-1:
                        fout.write(u' ')
                    else:
                        fout.write(u'\n')

def base_filter():
    f = string.punctuation
    f = f.replace("'", '')
    f += '\t\n'
    return f

def text_to_word_sequence(text, filters=base_filter(), lower=True, split=" "):
    if lower:
        text = text.lower()
    translate_table = dict((ord(char), None) for char in filters)
    text = text.translate(translate_table)
    seq = text.split(split)
    return [_f for _f in seq if _f]

def text2sequence(text):
        '''
        Convert a string into a list of words, filtering punctuations and irrelevant symbols
        :param text(a string):
        :return a list of words:
        '''
        global number_of_tokens
        sequence = text_to_word_sequence(text, filters=base_filter(), lower=True, split=" ")
        for i in range(len(sequence)):
            sequence[i]=re.sub(r'^[0-9]+$','<NUMBER>',sequence[i])
            # converts links to <URL>
            sequence[i] = re.sub(r'(https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*', '<URL>', sequence[i])
            number_of_tokens+=1
        return sequence

def generate(obj, min_score, min_length):
    global number_of_comments
    number_of_comments+=1
    if number_of_comments%100000==0:
            print(number_of_comments)
            #print(repr((number_of_comments-last_number_of_comments)/duration )+" comments per second" )
            #last_number_of_comments=number_of_comments

    if (obj['subreddit'] in SELECTED_SUBREDDIT or not SELECTED_SUBREDDIT) \
    and obj['score'] > min_score:
        sequences=[]
        global number_of_tokens
        number_of_tokens+=1

        body = getString(obj)
        if body == '[deleted]':
            return
        else:
            sentences=string2sentences(body)
        for sentence in sentences:
            sequences.append(text2sequence(sentence))

        if sum(len(x) for x in sequences) > min_length:
            if not SELECTED_SUBREDDIT:
                write(FOUT_PATH, sequences)
            else:
                comment = [word for sentence in sequences for word in sentence]
                for word in set(comment):
                    if word in IDF_DICT:
                        IDF_DICT[word] += 1
                    else:
                        IDF_DICT[word] = 1 
                party = obj['subreddit']
                space = " "
                with codecs.open('./data/'+party+'.sub', 'ab', 'utf-8') as sub:
                    sub.write(space.join(comment))
                    sub.write(u'\n')
                with codecs.open('./data/'+party+'.aut', 'ab', 'utf-8') as author:
                    author.write(obj['author'])
                    author.write(u'\n')
