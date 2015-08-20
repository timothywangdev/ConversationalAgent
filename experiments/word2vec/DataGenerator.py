__author__ = 'Hujie Wang'

import json
import re


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
        with open('./data/data.json', encoding='utf-8') as data_file:
            data = json.loads(data_file.read(),cls=ConcatJSONDecoder)
        return data

    def getSentences(self,data):
        '''
        Return a list of sentences(string) given a JSON data

        :param data (JSON)
        :return: a list of strings
        '''

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