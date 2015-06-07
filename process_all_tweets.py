# This script looks through samples of tweets from the mongo collection called
# random_sample_june7th in the tweets database, and categorizes each tweet as
# spam or not spam.
import tweetPreprocessor
from pymongo import MongoClient

# Establish mongo info:
client = MongoClient()
db = client.tweets
collect = db.random_sample_june7th

# Pick up a bunch of tweets:
found = collect.find({ 'spam_rating' : { '$exists' : False } } )

# Turn them into two lists: one of ids, one of tweet text:
tweet_ids = []
tweet_texts = []
while found.alive == True:
    tweet = found.next()
    tweet_texts.append(tweet['text'])
    tweet_ids.append(tweet['id'])

db1 = tweetPreprocessor.tweetDatabase(tweet_texts)
db1.identify_spam()
db1.strip_and_lower_spam()
spam_indices = db1.spam_indices
spam_tweets = db1.spam_tweets_stripped_and_lowered

# Use ids to insert spam_rating back into database:
for tweet_index in range(len(tweet_ids)): # tweet_index is the id of the tweet in the python file!
    t_id = tweet_ids[tweet_index] # t_id is the id of the tweet in the mongodb!
    if tweet_index in spam_indices:
        collect.update({ 'id' : t_id}, {'spam_rating' : 1}, { 'upsert' : False})
    else:
        collect.update({ 'id' : t_id}, {'spam_rating' : 0}, { 'upsert' : False})




