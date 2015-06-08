# This script discovers spam in tweets about major brands and writes it to disk.
# The spam is in stripped/lowercased sorted order.
import tweetPreprocessor
from pymongo import MongoClient
import time

# Establish mongo info:
client = MongoClient()
db = client.tweets
collect = db.test_collection

# Make list of major brands:
major_brands_list = ['google', 'twitter', 'facebook', 'apple', 'tumblr', 'disney',
                     'microsoft', 'bmw', 'youtube', 'nike', 'starbucks', 'nfl',
                     'nba', 'bbc', 'adobe', 'mtv', 'ford', 'playstation', 'xbox',
                     'walmart', 'mercedes', 'samsung', 'buzzfeed', 'abc', 'nasa',
                     'amazon', 'sony', 'mcdonalds', 'nintendo', 'chipotle', 'cnn',
                     'gucci', 'paypal']

# Make list of products:

# Get dataset for each major brand and product:
brand_data = {}
for brand in major_brands_list[:2]:
    found = db.test_collection.find( {'$text' : { '$search' : brand}})
    brand_data[brand] = []
    while found.alive == True:
        brand_data[brand].append(found.next()['text'])

spam_tweets = {}
for brand in major_brands_list[:2]:
    tweetsdb = tweetPreprocessor.tweetDatabase(brand_data[brand])
    tweetsdb.identify_spam()
    tweetsdb.strip_and_lower_spam()
    spam_tweets[brand] = tweetsdb.spam_tweets_stripped_and_lowered

# Detect spam and get stats on it:



# Print spam and stats on it to disk:

def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

def printer(path, brand_name, data_to_print):
    with open(path + 'spam_from_%s.txt' % brand_name, 'w') as outfile:
        for datapoint in data_to_print:
            outfile.write(remove_non_ascii(datapoint) + '\n')

path = '/Users/ilya/Projects/twitter_spam/brand_spam_data/'