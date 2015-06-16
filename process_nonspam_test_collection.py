# This script looks through the non-spam tweets from the test_collection and tries
# to spamify them. What will happen?
import tweetPreprocessor
from pymongo import MongoClient
import time
import math
from random import random

# Establish mongo info:
client = MongoClient()
db = client.tweets
collect = db.test_collection

# Pick up a bunch of tweets, but only if there are at least 10000 in there:
def spam_run():
    """Takes a random collection of tweets that haven't yet been run through the
    spam run number and runs them through the spam detector, 10k at a time, if 
    there are at least 10k that haven't yet been put through that run."""

    docs_not_yet_included_in_this_run = collect.count( { '$and' : [{'spam_rating' : 0},{'tweet_processor_version' : 2}] } )
    if docs_not_yet_included_in_this_run >= 10000:
        tweet_ids = []
        tweet_texts = []
        for x in range(10000):
            if x % 100 == 0: print 'filled %r random tweets into bucket' % x
            docs_to_skip = math.floor(random() * docs_not_yet_included_in_this_run/5)
            # Grab a single random tweet that doesn't have the spam_random_run1 field:
            tweet = collect.find( { '$and' : [{'spam_rating' : 0},{'tweet_processor_version' : 2}] } ).limit(1).skip(int(docs_to_skip)).next()
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
            if tweet_index % 100 == 0: print 'inserted %r tweets BACK into mongo' % tweet_index
            if tweet_index in spam_indices:
                collect.update({ '_id' : t_id}, {'$set' : { 'spam_rating_on_nonspam' : 1}}, False)
            else:
                collect.update({ '_id' : t_id}, {'$set' : { 'spam_rating_on_nonspam' : 0}}, False)

spam_run()
spam_run()
spam_run()
spam_run()
spam_run()