__author__ = 'Hujie Wang'
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
import numpy as np

class Classifier(object):
    '''
    Only supports MultinomialNB right now, more models will be added later
    MultinomialNB: Training accuracy: 0.765488302126 Testing accuracy: 0.688398052488
    '''
    def __init__(self):
        c=4

    def getTrainingData(self,fname,label):
        X=[]
        with open(fname,'r') as f:
            for line in f:
                X.append(line)
        y=[label]*len(X)
        return X,y

    def getAllTrainingData(self,fnames=['./data/Conservative.sub','./data/Liberal.sub','./data/progressive.sub','./data/republicans.sub','./data/socialism.sub'], labels=[1,0,0,1,0]):
        X=[]
        y=[]
        for i in range(len(fnames)):
            _X,_y=self.getTrainingData(fnames[i],labels[i])
            X+=_X
            y+=_y
        return X,y

    def fit(self,X,y):

        self.count_vect = CountVectorizer()
        self.X_train_counts = self.count_vect.fit_transform(X)
        self.tfidf_transformer = TfidfTransformer()
        X_train_tfidf = self.tfidf_transformer.fit_transform(self.X_train_counts)
        self.clf = MultinomialNB().fit(X_train_tfidf, y)

    def predict(self,X):
        X_new_counts = self.count_vect.transform(X)
        X_new_tfidf = self.tfidf_transformer.transform(X_new_counts)
        return self.clf.predict(X_new_tfidf)

    def evaluate(self,X,y):
        predicted_y=self.predict(X)
        return np.mean(predicted_y == y)


clf=Classifier()
X,y = clf.getAllTrainingData()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25)
clf.fit(X_train,y_train)
train_acc=clf.evaluate(X_train,y_train)
eva_acc=clf.evaluate(X_test,y_test)

print('Training accuracy: {} Testing accuracy: {}'.format(train_acc,eva_acc))
#print(clf.predict(['I like liberal']))
