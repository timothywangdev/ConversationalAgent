__author__ = 'Hujie Wang'

import json
import re
import time
import string
import codecs

from progressbar import Bar, ETA, Percentage, ProgressBar, RotatingMarker

FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)
FOUT_PATH="./data/data_generated"
SELECTED_SUBREDDIT=[]
number_of_tokens=0
number_of_comments=0
last_number_of_comments=0
start_time=None

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

        widgets = ['Speed: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
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
                generate(obj)
                pbar.update(nline+1)
                nline+=1
        pbar.finish()

        print('Data generation completed!')
        print('Number of comments:'+str(number_of_comments))
        print('Number of tokens:'+str(number_of_tokens))

def getString(obj):
        '''
        Return a list of strings given a JSON data

        :param data (JSON)
        :return: a list of stringswjwsz
        '''
        global number_of_comments
        global start_time
        global last_number_of_comments
        number_of_comments+=1
        current_time=time.time()
        #duration=int((current_time - start_time)*1000)
        if number_of_comments%100000==0:
            print(number_of_comments)
            #print(repr((number_of_comments-last_number_of_comments)/duration )+" comments per second" )
            #last_number_of_comments=number_of_comments
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
        Convert a string into a list of words, filtering punctuations and irreverent symbols
        :param text(a sttring):
        :return a list of words:
        '''
        global number_of_tokens
        sequence = text_to_word_sequence(text, filters=base_filter(), lower=True, split=" ")
        for i in range(len(sequence)):
            sequence[i]=re.sub(r'^[0-9]+$','<NUMBER>',sequence[i])
            number_of_tokens+=1
        return sequence

def generate(obj):
    if obj['subreddit'] in SELECTED_SUBREDDIT or not SELECTED_SUBREDDIT:
        sequences=[]
        global number_of_tokens
        number_of_tokens+=1
        sentences=string2sentences(getString(obj))
        for sentence in sentences:
            sequences.append(text2sequence(sentence))
        if not SELECTED_SUBREDDIT:
            write(FOUT_PATH, sequences)
        else:
            party = obj['subreddit']
            write('./data/'+party+'.sub', sequences)
            with open('./data/'+party+'.aut', 'a') as author:
                author.write(obj['author'])
                author.write('\n')
