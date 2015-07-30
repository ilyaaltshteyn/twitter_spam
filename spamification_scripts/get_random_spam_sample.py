# This script grabs a random bunch of spam tweets from the mongo database and
# writes them to a file. Useful for inspecting the output of the spam detector.
# CAUTION: randomness may be affected by what tweets are indexed by, because
# mongo stores indices in order.

import tweetPreprocessor
from pymongo import MongoClient
import time
import math
from random import random

# Establish mongo info:
client = MongoClient()
db = client.tweets
collect = db.test_collection

docs_not_yet_included_in_this_run = collect.count( { 'spam_rating' : 1 } )
tweet_ids = []
tweet_texts = []
for x in range(300):
    print 'filled %r random tweets into bucket' % x
    docs_to_skip = math.floor(random() * docs_not_yet_included_in_this_run)
    # Grab a single random tweet that doesn't have the spam_random_run1 field:
    tweet = collect.find( { 'spam_rating' : 1 } ).limit(1).skip(int(docs_to_skip)).next()
    tweet_texts.append(tweet['text'])
    tweet_ids.append(tweet['_id'])

stripped_tweets = []
for t1 in range(len(tweet_texts)):
    t = tweetPreprocessor.singleTweet(tweet_texts[t1])
    t.strip_non_ascii()
    t.strip_newlines()
    print t.tweet
    stripped_tweets.append(t.tweet)
print stripped_tweets[:3]
print tweet_ids[:3]

with open('random_spam_tweets2.txt', 'w') as outfile:
    for x in range(len(tweet_texts)):
        outfile.write(str(tweet_ids[x]) + ',' + stripped_tweets[x] + '\n')
