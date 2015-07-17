__author__ = 'hujie'

from keras.preprocessing.text import text_to_word_sequence,base_filter
import numpy as np
import six.moves.cPickle
from keras.preprocessing import sequence
import os

class Tokenizer(object):
    def __init__(self,maxWords=1000):
        self.maxWords=maxWords
        self.wordCount={}
        self.encoder={}
        self.decoder={}

    def fit(self,texts):
        sequences=[]
        for text in texts:
            sequences.append(text_to_word_sequence(text))
        for seq in sequences:
            for word in seq:
                if word in self.wordCount:
                    self.wordCount[word]+=1
                else:
                    self.wordCount[word]=1
        wcounts = list(self.wordCount.items())
        wcounts.sort(key = lambda x: x[1], reverse=True)

        self.encoder['<PAD>']=0
        self.encoder['<END>']=1
        self.encoder['<UNK>']=2

        self.decoder[0]='<PAD>'
        self.decoder[1]='<END>'
        self.decoder[2]='<UNK>'

        self.wordCount.clear()
        for i in range(len(wcounts)):
            pair=wcounts[i]
            self.encoder[pair[0]]=i+3
            self.decoder[i+3]=pair[0]
            if i<self.maxWords:
                self.wordCount[pair[0]]=pair[1]

        print('Most Frequent 20 words:')
        for i in range(min(20,len(wcounts))):
            print(wcounts[i])

    def transform(self,texts):
        rv=[]
        for i in range(len(texts)):
            sequence=text_to_word_sequence(texts[i])
            if len(sequence)==0:
                rv.append([0])
                continue
            list_of_scalars=[]
            for j in range(len(sequence)):
                if sequence[j] not in self.wordCount:
                    list_of_scalars.append(self.encoder['<UNK>'])
                else:
                    list_of_scalars.append(self.encoder[sequence[j]])
            rv.append(list_of_scalars)
        return rv

    def toMatrix(self,texts,length=10):
         x=self.transform(texts)
         return sequence.pad_sequences(x, maxlen=length)

    def save(self,path="./Tokenizer.pkl"):
        print('Saving Tokenizer...')
        f = open(path, 'wb')
        six.moves.cPickle.dump((self.encoder,self.decoder,self.wordCount,self.maxWords), f)
        print('Saved.')

    def load(self,path="./Tokenizer.pkl"):
        print('Loading Tokenizer...')
        f = open(path, 'rb')
        data=six.moves.cPickle.load(f)
        self.encoder=data[0]
        self.decoder=data[1]
        self.wordCount=data[2]
        self.maxWords=data[3]
        f.close()
        print('Loaded.')

#==================Tests================================
'''
tk=Tokenizer(3)
texts=["a a a b c c c c d d","e e e e e e c f"]
tk.fit(["a a a b c c c c d d","e e e e e e c"])
#tk.load()
t=tk.transform(texts,5)
print(t)
tk.save()

pq=Tokenizer()
pq.load()
print(pq.transform(texts,5))
'''