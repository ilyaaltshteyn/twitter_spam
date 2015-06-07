#!/usr/bin/env python

from config import *
from TwitterAPI import TwitterAPI
import time
import os
from pymongo import MongoClient

# Establish mongo info:
client = MongoClient()
db = client.tweets
collect = db.random_sample_june7th

# Establish twitter info:
delay = 8 # seconds

api_details_path = '/Users/ilya/Projects/twitter_spam'
api_details = []
with open(api_details_path + '/api_details.txt', 'r') as a:
    info = a.readlines()
    api_details.append(info)
api_details = api_details[0][0].split(',')

consumer_key = api_details[0]
consumer_secret = api_details[1]
access_token_key = api_details[2]
access_token_secret = api_details[3]

while True:
    try:
        api = TwitterAPI(consumer_key, consumer_secret,
                         access_token_key, access_token_secret)
        r = api.request('statuses/sample', {'language' : 'en'})
        try:
            for item in r.get_iterator():
                if 'retweeted_status' not in item:
                    collect.insert(item)
                delay = max(8, delay/2)
        except: 
            continue
    except:
        print "Error"
        print time.ctime()
        print "Waiting " + str(delay) + " seconds"
        time.sleep(delay)
        delay *= 2