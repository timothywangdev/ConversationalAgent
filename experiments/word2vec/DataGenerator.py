__author__ = 'Hujie Wang'

import json
import re
import keras.preprocessing.text as T

FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)

class ConcatJSONDecoder(json.JSONDecoder):
    def decode(self, s, _w=WHITESPACE.match):
        s_len = len(s)

        objs = []
        end = 0
        while end != s_len:
            obj, end = self.raw_decode(s, idx=_w(s, end).end())
            end = _w(s, end).end()
            objs.append(obj)
        return objs

class DataGenerator(object):
    def __init__(self,data_path):
        self.data_path=data_path

    def getData(self,fname):
        '''
        :param fname(Reddit comment JSON file):
        :return a dict of JSON object:
        '''
        with open(fname, encoding='utf-8') as data_file:
            data = json.loads(data_file.read(),cls=ConcatJSONDecoder)
        return data

    def getStrings(self,data):
        '''
        Return a list of strings given a JSON data

        :param data (JSON)
        :return: a list of strings
        '''

        list_of_strings=[]
        for item in data:
            list_of_strings.append(item['body'])
        return list_of_strings

    def string2sentences(self,str):
        '''
        :param str:
        :return a list of sentences:
        '''
        return [str]

    def write(self,fname,list_of_sentences):
        '''
        Append list of sentences(list of words) into a file(in binary), according to the data format of word2vec
        :param fname:
        :param l (list of strings):
        '''

    def text2sequence(self,text):
        '''
        Convert a string into a list of words, filtering punctuations and irreverent symbols
        :param text(a sttring):
        :return a list of words:
        '''
        return T.text_to_word_sequence(text, filters=T.base_filter(), lower=True, split=" ")

    def debug(self):
        data=self.getData("./data/data.json")
        strings=self.getStrings(data)
        sequences=[]
        for str in strings:
            sentences=self.string2sentence(str)
            for sentence in sentences:
                sequences.append(self.text2sequence(sentence))
        print(sequences[0:10])

d=DataGenerator("./data")
d.debug()
