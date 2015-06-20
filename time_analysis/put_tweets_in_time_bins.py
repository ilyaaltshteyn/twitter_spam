# This script assigns a time bin to every document in the test_collection. The
# time in a tweet is UTC time.

from pymongo import MongoClient

client = MongoClient()
db = client.tweets
collect = db.test_collection

found = db.test_collection.find()

count = 0
while found.alive == True:
    count +=1
    if count % 1000 == 0: print count
    tweet = found.next()
    t_id = tweet['_id']
    hr = float(tweet['collection_time'][:2])
    if float(tweet['collection_time'][3:5]) > 30:
        hr += .5
    collect.update({ '_id' : t_id}, {'$set' : {'collection_time_in_rounded_hours' : hr }}, False)

