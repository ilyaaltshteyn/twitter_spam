# This script pulls all spam out of mongo and runs a topic model on all of it.
from pymongo import MongoClient
import tweetPreprocessor
import gensim
from pprint import pprint
import nltk
import re
client = MongoClient()
db = client.tweets
collect = db.test_collection

found = db.test_collection.find({'spam_rating' : 1}).limit(10000)
print db.test_collection.count({'spam_rating' : 1})

def strip_tweet(tweet):
    """Replaces all non-ascii characters in the tweet with a space. Returns
    tweet."""
    tweet = tweet.replace('\n', '')
    username = re.compile(r"@\S+ ?")
    tweet = username.sub('', tweet)
    return ''.join([i if ord(i) < 128 else ' ' for i in tweet])

all_docs = []
with open('spam_sample.txt', 'w') as outfile:
    while found.alive == True:
        t = found.next()
        outfile.write(str(t['_id']) + ' ' + '1 ' + strip_tweet(t['text']) + '\n')

corpus = gensim.corpora.MalletCorpus('spam_sample.txt')
model = gensim.models.LdaModel(corpus, id2word=corpus.id2word, alpha=.1, num_topics=10)

pprint(model.show_topics(num_topics = 10, num_words = 3))