# Moves 2009 tweets into mongodb.
from pymongo import MongoClient
import tweetPreprocessor

# Get data out of textfile and put into mongo:

client = MongoClient()
db = client.tweets
collect = db.sample_from_2009


file_path = "/Users/ilya/Projects/twitter_spam/2009_data.txt"
with open(file_path, 'r') as infile:
    infile.readline() # Skip header
    for t in range(500000):
        if t % 1000 == 0: print t
        single_tweet = {}
        for l in range(6):
            line = infile.readline()
            if line[0] == 'T':
                single_tweet['time'] = line[2:-1]
            if line[0] == 'U':
                single_tweet['user'] = line[2:-1]
            if line[0] == 'W':
                single_tweet['text'] = line[2:-1]
            if line == '\n':
                if single_tweet['text'] == 'No Post Title':
                    break
                else:
                    collect.insert(single_tweet)
                    break

