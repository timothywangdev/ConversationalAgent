__author__ = 'hujie'

import os
import math

from sklearn.cross_validation import train_test_split
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
import numpy as np
from tqdm import tqdm
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
from keras.layers.embeddings import Embedding
import matplotlib.pyplot as plt
from keras.preprocessing import sequence
import six.moves.cPickle
import h5py

from preprocessing.Tokenizer import Tokenizer

class GenderClassifier(object):

    def __init__(self):

        '''
        Training parameters:
        '''
        self.batch_size=512
        self.minLen=50
        self.maxLen=200
        self.maxWords=50000
        self.max_features=self.maxWords+3
        self.nb_epoch=5

        self.trained=False
        self.modelLoaded=False
        self.dataPrepared=False

        self.tokenizer = Tokenizer(maxWords=self.maxWords)

        print('Build model...')

        self.model = Sequential()
        self.model.add(Embedding(self.max_features, 128))
        self.model.add(LSTM(input_dim=128, output_dim=128,return_sequences=True))
        self.model.add(Dropout(0.5))
        self.model.add(LSTM(input_dim=128, output_dim=128,return_sequences=True))
        self.model.add(Dropout(0.5))
        self.model.add(LSTM(input_dim=128, output_dim=128,return_sequences=False))
        self.model.add(Dense(input_dim=128, output_dim=1))
        self.model.add(Activation('sigmoid'))
        self.model.compile(loss='binary_crossentropy', optimizer='adam', class_mode="binary")

        print('Model has been built!')

    def load_data(self,dataSize=-1):
        import pandas as pd
        file_loc = os.path.dirname(os.path.realpath(__file__))
        relative_path = "blogger_data_2.csv" # move dataset to examples directory
        fullpath = os.path.join(file_loc, relative_path)
        if dataSize==-1:
            data=pd.read_csv(fullpath)
        else:
            data = pd.read_csv(fullpath, nrows=dataSize)
        X = data['text'].values
        X = [str(x) for x in X]
        y=data['gender'].values
        return X,y

    def prepareData(self,evaluate=False):
        print("Loading data...")
        X,y = self.load_data() # Can increase up to 250K or so
        print("Number of lines:", len(X))

        print("Vectorizing sequence data...")

        if not evaluate:
            self.tokenizer.fit(X)
            self.tokenizer.save("./data/Tokenizer.pkl")
        X=self.tokenizer.transform(X)



        _X=[]
        _y=[]

        for i in range(len(X)):
            if self.minLen<=len(X[i]) and len(X[i])<=self.maxLen:
                _X.append(X[i])
                _y.append(y[i])

        X=sequence.pad_sequences(_X, maxlen=self.maxLen)
        y=_y

        count_1=0
        for i in range(len(y)):
            if y[i]==1.0:
                count_1+=1
        print("female percentage:",(len(y)-count_1)/len(y))
        print("male percentage:",count_1/len(y))

        self.X_train, self.X_valid, self.y_train, self.y_valid = train_test_split(X, y, test_size=0.10, random_state=100)
        self.dataPrepared=True
        print("Data preparation completed!")

    def evaluate(self):
        '''
        For debugging purpose
        '''
        if not (self.modelLoaded or self.trained):
            print('Warning: Model data has not been loaded or the model has not been trained.')
            print("Trying to load Model dada...")
            self.loadModel()
        if not self.dataPrepared:
            self.prepareData(evaluate=True)

        score, acc = self.model.evaluate(self.X_valid, self.y_valid, batch_size=self.batch_size, show_accuracy=True)
        print("Evaluation results:", score, " ", acc)

    def train(self):
        if not self.dataPrepared:
            self.prepareData()

        checkpointer = ModelCheckpoint(filepath="./weights.hdf5", verbose=1, save_best_only=True)
        stopper=EarlyStopping(monitor='val_loss', patience=50, verbose=0)

        print("Training...")

        self.model.fit(self.X_train, self.y_train, batch_size=self.batch_size, nb_epoch=self.nb_epoch, validation_data=(self.X_valid,self.y_valid), show_accuracy=True,callbacks=[checkpointer,stopper])

        self.trained=True
        print('Training completed!')

    def loadModel(self):
        print('Loading model...')
        self.model.load_weights('./data/weights.hdf5')
        self.tokenizer.load("./data/Tokenizer.pkl")
        self.modelLoaded=True
        print('Model loaded')

    '''
    text: list or string
    return: vector of results
    '''
    def predict(self,text):
        if not (self.modelLoaded or self.trained):
            print('Warning: Model data has not been loaded or the model has not been trained.')
            print("Trying to load Model dada...")
            self.loadModel()

        X=np.array(self.tokenizer.transform(text))
        y=self.model.predict(X,batch_size=1)
        return y


#========================TESTS===================================
'''
clf=GenderClassifier()
#clf.evaluate()
print(clf.predict(["Even if you draw a room full of cool friends, he's still being a buzzkill staring at the floor. Also, there's no way that noose is going to hold him, he can\'t even hang a picture. What a failure."]))
'''