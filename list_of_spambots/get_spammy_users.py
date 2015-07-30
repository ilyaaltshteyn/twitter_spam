# This script makes a list of spammers who are likely spambots. It uses the following
# simple rules to determine who is a bot:
# 1. User has at least one spam tweet in the test_collection or random_sample_remote_computer
# 2. User's spam tweet is not about how many twitter followers they have.
# 3. User has at least 100 tweets. I experimented with different numbers here.
# So much room for improvement to the above rules, so little time.

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
# how many followers they gained/lost that day and aren't a retweet of the horoscope,
# a post of a new photo or video, etc. More stop words can be added here to prevent
# false-positive spambot ids.
spam_user_indices = []
for x in range(len(tweets)):
    if x % 1000 == 0: print 'Got indices for %r usernames' % x
    stop_words = ['follower', 'unfollow', 'followed', 'posted a new photo',
                  'posted a photo', 'stats', 'such a good', 
                  'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra',
                  'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces',
                  '&gt', '&lt', 'same', 'coo', 'high', 'why am', 'awake',
                  '11:11', 'happy birthday', 'text me', 'hate', 'my god', 'so much',
                  'so hot', 'ask me a', 'i want some', 'wanna go', 'love', 'hate',
                  'what is this', 'bored', 'sleep', 'send me', 'friday', 'a nap',
                  'fuck this', 'fuck him', 'fuck her', 'fuck you', 'roundteam',
                  'my best rt', 'talk to', 'honestly', 'what to do', 'the beach',
                  'need to go', 'me off', 'this sucks', 'what it is', 'welcome',
                  'my gosh', 'younow', 'happy rn', 'sad rn', 'tired rn', 'hungry rn',
                  'dj name', 'added a video']
    real_human = 0
    for stop_word in stop_words:
        if stop_word in tweets[x].lower():
            real_human = 1
            break
    if real_human == 0:
        spam_user_indices.append(x)

# Now get usernames and statuses counts of spambots:
spambot_usernames = []
# spambot_username_statuses_counts = [] # The mean of this is about 25k
count_of_spam_tweets_by_humans = 0
counter = 0
print 'About to look through %r users to find spambots and count of spam tweets by humans' % len(spam_user_indices)

for i in spam_user_indices:
    counter += 1
    if counter % 1000 == 0: print 'Got usernames and statuses counts of %r spammy users/spambots' % counter
    if users[i]['screen_name'] not in spambot_usernames and users[i]['statuses_count'] > 100:
        spambot_usernames.append(users[i]['screen_name'])
        # spambot_username_statuses_counts.append(users[i]['statuses_count'])
    elif users[i]['screen_name'] not in spambot_usernames and users[i]['statuses_count'] <= 100:
        count_of_spam_tweets_by_humans += 1

print 'number of spambots in dataset: %r' % len(set(spambot_usernames)) # Number of spambots in dataset = 17591

with open('spambots_list.txt', 'w') as outfile:
    for spambot in spambot_usernames:
        outfile.write(spambot + '\n')
