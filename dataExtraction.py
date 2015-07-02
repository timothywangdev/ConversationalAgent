__author__ = 'Hujie'

import praw

'''
Parameters: submission object, limit of number of comments
Returns: a comment forest which contains all comments in the submission

Due to API delay, it may take a while.
'''
def getComments(submission,limit=100):
    submission.replace_more_comments(limit=limit, threshold=0)
    all_comments = submission.comments
    return all_comments

'''
Prints all comments in comments, for debugging purposes
Parameters: comments object
Returns: none
'''
def showComments(comments):
    flat_comments = praw.helpers.flatten_tree(comments)
    for comment in flat_comments:
        print(comment.body)
'''
Parameters: subreddit string, limit of number of submissions
Returns: list of submissions
'''
def getSubmissions(subreddit_str,limit=100):
    subreddit = r.get_subreddit(subreddit_str)
    return subreddit.get_hot(limit=limit)

user_agent = ("Linux:ConversationalAgentTools:0.0.1 (by /u/0x00FFFF00)")
r = praw.Reddit(user_agent=user_agent)

submissions=getSubmissions("learnpython")
for submission in submissions:
    showComments(getComments(submission))


