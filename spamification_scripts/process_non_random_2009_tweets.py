# This script looks through non-random samples of the sample_from_2009 tweets
# collection and spamifies them.
import tweetPreprocessor
from pymongo import MongoClient
import time
import math
from random import random

# Establish mongo info:
client = MongoClient()
db = client.tweets
collect = db.sample_from_2009

# Pick up a bunch of tweets, but only if there are at least 5000 in there:
while True:
    found = collect.find({'spam_rating' : {'$exists' : False}}).limit(10000)

    # Turn them into two lists: one of ids, one of tweet text:
    tweet_ids = []
    tweet_texts = []
    while found.alive == True:
        tweet = found.next()
        tweet_texts.append(tweet['text'])
        tweet_ids.append(tweet['_id'])

    db1 = tweetPreprocessor.tweetDatabase(tweet_texts, batch_size = 10000)
    db1.identify_spam()
    db1.strip_and_lower_spam()
    spam_indices = db1.spam_indices
    spam_tweets = db1.spam_tweets_stripped_and_lowered

# Use ids to insert spam_rating back into database:
    for tweet_index in range(len(tweet_ids)): # tweet_index is the id of the tweet in the python file!
        t_id = tweet_ids[tweet_index] # t_id is the id of the tweet in the mongodb!
        if tweet_index % 100 == 0: print 'finished %r tweets' % str(tweet_index)
        if tweet_index in spam_indices:
            collect.update({ '_id' : t_id}, {'$set' : {'spam_rating' : 1, 'tweet_processor_version' : 2}}, False)
        else:
            collect.update({ '_id' : t_id}, {'$set' : {'spam_rating' : 0, 'tweet_processor_version' : 2}}, False)