# This script makes a list of spammers who are likely spambots. It uses the following
# simple rules to determine who is a bot:
# 1. User has at least one spam tweet in the test_collection.
# 2. User's spam tweet is not about how many twitter followers they have.
# 3. User has at least 10k tweets.

import tweetPreprocessor
from pymongo import MongoClient
import time
import math
import numpy as np
from random import random

# Establish mongo info:
client = MongoClient()
db = client.tweets
collect = db.test_collection

# Get all tweets that were previously IDed as spam tweets, and count the ones
# that were IDed as non-spam:
found = collect.find( {'spam_rating' : 1} )
users = []
tweets = []
while found.alive == True:
    tweet = found.next()
    users.append(tweet['user'])
    tweets.append(tweet['text'])

print 'stage 1 complete'

detected_spam_tweets_count = len(tweets)
# Get the indices for the usernames and tweet texts of tweets that aren't about
# how many followers they gained/lost that day:
spam_user_indices = []
for x in range(len(tweets)):
    if x % 1000 == 0: print 'Got indices for %r usernames' % x
    if 'today stats' not in tweets[x] and 'followers' not in tweets[x] and 'unfollowed' not in tweets[x] and 'followed' not in tweets[x] and 'posted a new photo' not in tweets[x]:
        spam_user_indices.append(x)

# Store the number of tweets that you threw out because they were from non-bots:
thrown_out_spam_tweets_count = detected_spam_tweets_count - len(spam_user_indices)
# You threw out 1013 tweets

# Now get usernames and statuses counts of spambots:
spambot_usernames = []
spambot_username_statuses_counts = [] # The mean of this is about 25k
count_of_spam_tweets_by_humans = 0
counter = 0
print 'About to look through %r users to find spambots and count of spam tweets by humans' % len(spam_user_indices)
for i in spam_user_indices:
    counter += 1
    if counter % 1000 == 0: print 'Got usernames and statuses counts of %r spammy users/spambots' % counter
    if users[i]['screen_name'] not in spambot_usernames and users[i]['statuses_count'] > 10000:
        spambot_usernames.append(users[i]['screen_name'])
        spambot_username_statuses_counts.append(users[i]['statuses_count'])
    elif users[i]['screen_name'] not in spambot_usernames and users[i]['statuses_count'] <= 10000:
        count_of_spam_tweets_by_humans += 1

print np.mean(np.array(spambot_username_statuses_counts)) # Spambots mean tweets count = 36611
print np.median(np.array(spambot_username_statuses_counts)) # Spambots median tweets count = 22182
print len(set(spambot_usernames)) # Number of spambots in dataset = 17591
print 'stage 2 complete'

# Now find out how many statuses there are by the spambots in the dataset:
all_spam = []
counter = 0
for username in set(spambot_usernames):
    counter += 1
    if counter % 1000 == 0 : print 'looked through %r users' % counter
    found = collect.find({ 'user.screen_name' : username})
    while found.alive == True:
        all_spam.append(found.next()['text'])

print len(all_spam) # This is the number of spam tweets by the spambots = 55385
complete_spam_list_length = len(all_spam) + thrown_out_spam_tweets_count + count_of_spam_tweets_by_humans
all_tweets_count = collect.count({'spam_rating' : {'$exists' : True}})

# 10.75% are spam if we consider any tweet from a bot as spam:
print float(complete_spam_list_length) / all_tweets_count 

# 8.88% are spam if we just look at the spam that the approx nearest neighbors search found:
print float(collect.count({'spam_rating' : 1})) / ( collect.count({'spam_rating' : 1}) + collect.count({'spam_rating' : 0}))



