# ConversationalAgent
Conversational Agent

# Installation
* Install progressbar library with "pip install progressbar"
* Add project dir to root user's PATH variable or local user's PATH variable depending on your python configuration

# Usage
DataGenerator.py contains a "do" method which is the main utility. It takes a reddit data file (json format, from praw) and a subreddit filter, and outputs a compiled corpus. The corpus can then be fed into the word2vec exe compiled from google code.