from pymongo import MongoClient
import tweetPreprocessor
import ast
client = MongoClient()
db = client.tweets
collect = db.random_sample_remote_computer

path = "/Users/ilya/Projects/twitter_spam/"
filename = "remote_computer_tweets_sample.txt"
file_length = sum(1 for line in open(path + filename))
with open(path + filename, 'r') as infile:
    print len(infile)
    for x in xrange(file_length - 1):
        if x % 10000 == 0 : print x
        try:
            tweet = ast.literal_eval(infile.next())
            # collect.insert(tweet)
        except:
            continue