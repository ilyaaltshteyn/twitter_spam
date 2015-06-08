import tweetPreprocessor
from pymongo import MongoClient
import time
import math
from random import random

# Establish mongo info:
client = MongoClient()
db = client.tweets
collect = db.random_sample_june7th

# Get all tweets that were previously IDed as spam tweets, and count the ones
# that were IDed as non-spam:
found = collect.find()
all_found = []
non_spam_count = 0
while found.alive == True:
    tweet = found.next()
    if 'spam_rating' in tweet and tweet['spam_rating'] == 1:
        all_found.append(tweet)
    if 'spam_rating' in tweet and tweet['spam_rating'] == 0:
        non_spam_count += 1
print len(all_found)

# Pull user info and tweet text from the spam tweets:
users = []
tweets = []
for f in all_found:
    users.append(f['user'])
    tweets.append(f['text'])
del all_found

detected_spam_tweets_count = len(tweets)
# Get the indices for the usernames and tweet texts of tweets that aren't about
# how many followers they gained/lost that day:
spam_user_indices = []
for x in range(len(tweets)):
    if 'today stats' not in tweets[x] and 'followers' not in tweets[x] and 'unfollowed' not in tweets[x]:
        spam_user_indices.append(x)

# Store the number of tweets that you threw out because they were from actual users:
thrown_out_spam_tweets_count = detected_spam_tweets_count - len(spam_user_indices)
# You threw out 1013 tweets

# Get the actual "user" section of each tweet for the spambots:
spam_user_info = []
for i in spam_user_indices:
    spam_user_info.append(users[i])

# Now get the actual usernames of the spammers, and each one's total statuses count:
spam_usernames = []
spam_username_statuses_counts = [] # The mean of this is about 25k
for user in spam_user_info:
    if user['screen_name'] not in spam_usernames and user['statuses_count'] > 500:
        spam_username_statuses_counts.append(user['statuses_count'])
        spam_usernames.append(user['screen_name'])

# Now find out how many statuses there are by those users in the dataset:
all_spam = []
counter = 0
for username in set(spam_usernames):
    counter += 1
    if counter % 100 == 0 : print 'looked through %r users' % counter
    found = collect.find({ 'user.screen_name' : username})
    while found.alive == True:
        all_spam.append(found.next())

print len(all_spam) # This is the number of spam tweets by the spambots
complete_spam_list_length = len(all_spam) + thrown_out_spam_tweets_count
print float(complete_spam_list_length) / (complete_spam_list_length + non_spam_count)

# 7.2% of tweets are spam.


