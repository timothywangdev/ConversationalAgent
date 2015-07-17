__author__ = 'hujie'

from GenderClassifier import GenderClassifier

clf=GenderClassifier()

while True:
     print(clf.predict([input("Enter text: ")]))


