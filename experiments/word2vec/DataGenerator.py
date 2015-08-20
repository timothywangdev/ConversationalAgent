__author__ = 'Hujie Wang'

import json
import re
import keras.preprocessing.text as T
from tqdm import tqdm

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

    def getData(self,fname):
        '''
        :param fname(Reddit comment JSON file):
        :return a dict of JSON object:
        '''
        with open(fname) as data_file:
            data = json.loads(data_file.read(),cls=ConcatJSONDecoder)
        return data

    def getStrings(self,data):
        '''
        Return a list of strings given a JSON data

        :param data (JSON)
        :return: a list of strings
        '''

        list_of_strings=[]
        for i in range(len(data)):
            list_of_strings.append(data[i]['body'])
        return list_of_strings

    def string2sentences(self,str):
        '''
        :param str:
        :return a list of sentences:
        '''
        return list(filter(bool,re.split(r'[;,.!?]+',str)))


    def write(self,fname,sequences):
        '''
        Append list of tokens into a file(in binary), according to the data format of word2vec
        :param fname:
        :param l (list of strings):
        '''
        print('Writing data into '+fname)
        with open(fname,'wb') as fout:
            for i in tqdm(range(len(sequences))):
                for j in range(len(sequences[i])):
                    fout.write(bytes(sequences[i][j], 'UTF-8'))
                    if j!=len(sequences[i])-1:
                        fout.write(bytes(' ', 'UTF-8'))
                    else:
                        fout.write(bytes('\n', 'UTF-8'))

    def text2sequence(self,text):
        '''
        Convert a string into a list of words, filtering punctuations and irreverent symbols
        :param text(a sttring):
        :return a list of words:
        '''
        sequence = T.text_to_word_sequence(text, filters=T.base_filter(), lower=True, split=" ")
        for i in range(len(sequence)):
            sequence[i]=re.sub(r'^[0-9]+$','<NUMBER>',sequence[i])
            self.number_of_tokens+=1
        return sequence

    def generate(self,fin_path,fout_path):

        self.number_of_tokens=0

        data=self.getData(fin_path)
        strings=self.getStrings(data)
        sequences=[]
        self.number_of_comments=len(strings)
        print('Converting reddit comments into tokens...')
        for i in tqdm(range(len(strings))):
            sentences=self.string2sentences(strings[i])
            for sentence in sentences:
                sequences.append(self.text2sequence(sentence))
        self.write(fout_path,sequences)
        print('Data generation completed!')
        print('Number of comments:'+str(self.number_of_comments))
        print('Number of tokens:'+str(self.number_of_tokens))


d=DataGenerator()
d.generate("./data/data.json","./data/data_generated")



