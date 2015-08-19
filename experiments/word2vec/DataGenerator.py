__author__ = 'Hujie Wang'

import json

class DataGenerator(object):
    def __init__(self,data_path):
        self.data_path=data_path

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