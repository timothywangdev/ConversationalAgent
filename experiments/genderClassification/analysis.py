__author__ = 'hujie'

from experiments.genderClassification.GenderClassifier import GenderClassifier
from preprocessing.DataExtraction import DataExtraction
import numpy as np
import praw
import json
import matplotlib.pyplot as plt
from tqdm import tqdm
import os

np.random.seed(seed=5)

topics=[]
de=DataExtraction()

def prepare_topic(subreddit_str="uwaterloo",num_of_topics=10,fname=None,save=False,save_fname="data.txt"):
    topics=[]
    if fname != None:
        with open(fname, 'r') as infile:
            data=json.load(infile)
        return data

    submissions=de.getSubmissions(subreddit_str,limit=num_of_topics)
    topic_count=0
    for submission in submissions:
        allComments=de.getComments(submission,limit=100)
        flat_comments = praw.helpers.flatten_tree(allComments)
        comments_str=[]
        for comment in flat_comments:
            comments_str.append(comment.body)
        if len(comments_str)>0:
            topics.append({"title":submission.title,"text":submission.selftext,"comments":comments_str})
            topic_count+=1
        if topic_count>=num_of_topics:
            break

    if save:
        with open(save_fname, 'w') as outfile:
            json.dump(topics, outfile)
    return topics

def getRandomCommentFromRandomTopic(topics,minLen=50,maxLen=800):
    while True:
        comment=getRandomComment(topics,np.random.randint(len(topics)))
        if minLen<=len(comment) and len(comment)<=maxLen:
            return comment

def getRandomComment(topics,topic_id):
    assert(len(topics[topic_id]['comments'])!=0)
    return topics[topic_id]['comments'][np.random.randint(len(topics[topic_id]['comments']))]


'''
topics_battlefield=prepare_topic(subreddit_str="battlefield",num_of_topics=100,fname=None,save=True,save_fname="battlefield.txt")
topics_femalefashion=prepare_topic(subreddit_str="femalefashionadvice",num_of_topics=100,fname=None,save=True,save_fname="femalefashion.txt")
'''


topics_battlefield=prepare_topic(subreddit_str="battlefield",num_of_topics=100,fname="./data/battlefield.txt",save=True,save_fname="battlefield.txt")
topics_femalefashion=prepare_topic(subreddit_str="femalefashionadvice",num_of_topics=100,fname="data/femalefashion.txt",save=True,save_fname="femalefashion.txt")


distribution_battlefield=[]
distribution_femalefashion=[]


clf=GenderClassifier()
for i in tqdm(range(10000)):
    prob_1=clf.predict([getRandomCommentFromRandomTopic(topics_battlefield)])
    prob_2=clf.predict([getRandomCommentFromRandomTopic(topics_femalefashion)])
    #print(prob_1[0])
    #print(prob_2[0])
    distribution_battlefield.append(round(prob_1[0,0]*100))
    distribution_femalefashion.append(round(prob_2[0,0]*100))


f, g = plt.subplots(2,sharex=True,sharey=True)
g[0].hist(distribution_battlefield, 50, histtype='bar')
g[0].set_title("battlefield")
g[0].set_xlabel('Male<---probability*100--->Female')
g[0].set_ylabel('Frequency')
g[1].hist(distribution_femalefashion, 50, histtype='bar')
g[1].set_title("femalefashion")
g[1].set_xlabel('Male<---probability*100--->Female')
g[1].set_ylabel('Frequency')

plt.show()

'''
plt.hist(distribution_femalefashion)
plt.title("Gaussian Histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()
'''