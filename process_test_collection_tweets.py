# This script looks through samples of tweets from the mongo collection called
# test_collection in the tweets database, and categorizes each tweet as
# spam or not spam.
import tweetPreprocessor
from pymongo import MongoClient
import time

# Establish mongo info:
client = MongoClient()
db = client.tweets
collect = db.test_collection

# Pick up a bunch of tweets, but only if there are at least 10k in there:
while True:
    if collect.count( {'$and' : [{ 'tweet_processor_version' : { '$exists' : False } },
                                 { 'text' : { '$exists' : True }},
                                 { 'user' : { '$exists' : True }} ] } ) >= 10000:
        found = collect.find( {'$and' : [{ 'tweet_processor_version' : { '$exists' : False } },
                                 { 'text' : { '$exists' : True }},
                                 { 'user' : { '$exists' : True }} ] } ).limit(10000)

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

        # If there aren't at least 5000 tweets to work with, then break:
    else:
        break
