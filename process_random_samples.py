# This script identifies spam in a random sample of tweets from the mongo database.
# It does this on a collection of 10000 tweets at a time. After a tweet has been
# included in a random sample once, it can't be included in a random sample again
# until the next run.

import tweetPreprocessor
from pymongo import MongoClient
import time
import math
from random import random

# Establish mongo info:
client = MongoClient()
db = client.tweets
collect = db.random_sample_june7th

# First, add a random number to each document for each run.

# def add_random_numbers():
#     """Adds 3 fields to each document that doesn't yet have them, up to 5k documents.
#     Each of the 3 fields contains a random integer between 1k and 10k. The fields
#     are called random_number_1, random_number_2, and random_number_3. """
    
#     found = collect.find( { 'random_number_1' : { '$exists' : False } } ).limit(5000)
#     while found.alive == True:
#         try:
#             next_one = found.next()
#             mongo_id = next_one['_id']
#             next_one['random_number_1'] = randint(1000,10000)
#             collect.update({'_id':mongo_id}, {"$set": next_one}, upsert = False)
#         except:
#             break

#     found = collect.find( { 'random_number_2' : { '$exists' : False } } ).limit(5000)
#     while found.alive == True:
#         try:
#             next_one = found.next()
#             mongo_id = next_one['_id']
#             next_one['random_number_2'] = randint(1000,10000)
#             collect.update({'_id':mongo_id}, {"$set": next_one}, upsert = False)
#         except:
#             break

#     found = collect.find( { 'random_number_3' : { '$exists' : False } } ).limit(5000)
#     while found.alive == True:
#         try:
#             next_one = found.next()
#             mongo_id = next_one['_id']
#             next_one['random_number_3'] = randint(1000,10000)
#             collect.update({'_id':mongo_id}, {"$set": next_one}, upsert = False)
#         except:
#             break

# add_random_numbers()

# Pick up a bunch of tweets, but only if there are at least 10000 in there:
def spam_run(run_number):
    """Takes a random collection of tweets that haven't yet been run through the
    spam run number and runs them through the spam detector, 10k at a time, if 
    there are at least 10k that haven't yet been put through that run."""
    if run_number == 1: 
        spam_run = 'spam_random_run1'
    elif run_number == 2:
        spam_run = 'spam_random_run2'
    elif run_number == 3:
        spam_run = 'spam_random_run3'
    else: 
        raise(Exception('That run number is nonsense'))

    docs_not_yet_included_in_this_run = collect.count( { spam_run : { '$exists' : False } } )
    if docs_not_yet_included_in_this_run >= 10000:
        tweet_ids = []
        tweet_texts = []
        for x in range(10000):
            if x % 100 == 0: print 'filled %r random tweets into bucket' % x
            docs_to_skip = math.floor(random() * docs_not_yet_included_in_this_run)
            # Grab a single random tweet that doesn't have the spam_random_run1 field:
            tweet = collect.find({ spam_run : { '$exists' : False } } ).limit(1).skip(int(docs_to_skip)).next()
            tweet_texts.append(tweet['text'])
            tweet_ids.append(tweet['_id'])

        db1 = tweetPreprocessor.tweetDatabase(tweet_texts, batch_size = 10000, sensitivity = .4)
        db1.identify_spam()
        db1.strip_and_lower_spam()
        spam_indices = db1.spam_indices
        spam_tweets = db1.spam_tweets_stripped_and_lowered

    # Use ids to insert spam_rating back into database:
        for tweet_index in range(len(tweet_ids)): # tweet_index is the id of the tweet in the python file!
            t_id = tweet_ids[tweet_index] # t_id is the id of the tweet in the mongodb!
            if tweet_index % 100 == 0: print 'inserted %r tweets BACK into mongo' % tweet_index
            if tweet_index in spam_indices:
                collect.update({ '_id' : t_id}, {'$set' : { spam_run : 1}}, False)
            else:
                collect.update({ '_id' : t_id}, {'$set' : { spam_run : 0}}, False)

spam_run(3)
spam_run(1)
spam_run(2)
spam_run(3)
spam_run(1)
spam_run(2)
spam_run(3)
spam_run(1)
spam_run(2)
spam_run(3)
spam_run(1)
spam_run(2)
spam_run(3)
spam_run(1)
spam_run(2)
spam_run(3)
spam_run(1)
spam_run(2)
spam_run(3)
spam_run(1)
spam_run(2)
spam_run(3)
spam_run(1)
spam_run(2)
spam_run(3)
spam_run(1)
spam_run(2)
spam_run(3)
spam_run(1)
spam_run(2)
spam_run(3)
spam_run(1)
spam_run(2)
spam_run(3)
spam_run(1)
spam_run(2)
spam_run(3)
