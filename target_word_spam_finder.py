# This script discovers spam in tweets about major target_words and writes it to disk.
# The spam is in stripped/lowercased sorted order.
import tweetPreprocessor
from pymongo import MongoClient
import time
import copy

# Establish mongo info:
client = MongoClient()
db = client.tweets
collect = db.test_collection

# Make list of major brands/products/target words whose tweets you want to find:
target_words = ['itunes', 'androidgames', 'iphonegames', 'nyt', '"national enquirer"']

# Get dataset for each major target_word and product:
target_word_data = {}
for target_word in copy.copy(target_words):
    if db.test_collection.count( {'$text' : { '$search' : target_word}}) < 300:
        print "NOT ENOUGH TWEETS THAT INCLUDE THE WORD %s, SKIPPING" % target_word
        del target_words[target_words.index(target_word)]
        continue
    found = db.test_collection.find( {'$text' : { '$search' : target_word}}).limit(10000)
    print 'Working on the word "%r"' % target_word
    target_word_data[target_word] = []
    while found.alive == True:
        target_word_data[target_word].append(found.next()['text'])

def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])
path = '/Users/ilya/Projects/twitter_spam/target_word_spam_data/'

spam_tweets = {}
for target_word in target_words:
    tweetsdb = tweetPreprocessor.tweetDatabase(target_word_data[target_word])
    tweetsdb.identify_spam()
    tweetsdb.strip_and_lower_spam()
    spam_tweets[target_word] = tweetsdb.spam_tweets_stripped_and_lowered
    with open(path + 'v2_raw_spam_' + str(target_word), 'w') as outfile:
        for t in spam_tweets[target_word]:
            outfile.write(remove_non_ascii(t) + '\n')

spam_percent = {}
for target_word in target_words:
    spam_percent[target_word] = float(len(spam_tweets[target_word]))/len(target_word_data[target_word])

# Write spam percents to a masterfile:
with open('v2_target_word_spam_summary.txt', 'a') as outfile:
    for k, v in spam_percent.items():
        outfile.write(k + ',' + str(v) + '\n')

# Sort spam_percent dictionary by spam_percent:
# import operator
# sorted_spam_percents = sorted(spam_percent.items(), key=operator.itemgetter(1))

# Detect spam and get stats on it:


# Print spam and stats on it to disk:


def printer(path, target_word_name, total_data_count, percent_spam, sorted_spam):
    with open(path + 'v2_spam_from_%s.txt' % target_word_name, 'w') as outfile:
        outfile.write('There are %r tweets from %r, and they are %r spam' % (total_data_count, target_word_name, percent_spam * 100) + '\n')
        for datapoint in sorted_spam:
            outfile.write(remove_non_ascii(datapoint) + '\n')

for target_word in target_words:
    printer(path, target_word, len(target_word_data[target_word]), spam_percent[target_word], spam_tweets[target_word])



