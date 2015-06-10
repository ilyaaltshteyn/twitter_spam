#!/usr/bin/env python
# This script pulls a random 1% of english language tweets from Twitter.

from config import *
from TwitterAPI import TwitterAPI
import time
import os

# Establish twitter info:
delay = 8 # seconds

api_details_path = '/home/ilya/random_tweets'
api_details = []
with open(api_details_path + '/api_details.txt', 'r') as a:
    info = a.readlines()
    api_details.append(info)
api_details = api_details[0][0].split(',')

consumer_key = api_details[0]
consumer_secret = api_details[1]
access_token_key = api_details[2]
access_token_secret = api_details[3]

file_location = api_details_path + '/random_tweets.txt'

while True:
    try:
        api = TwitterAPI(consumer_key, consumer_secret,
                         access_token_key, access_token_secret)
        r = api.request('statuses/sample', {'language' : 'en'})
        with open(file_location, "a") as output:
            for item in r.get_iterator():
                if 'retweeted_status' not in item:
                    output.write(str(item) + "\n")
                    delay = max(8, delay/2)
    except:
        print "Error"
        print time.ctime()
        print "Waiting " + str(delay) + " seconds"
        time.sleep(delay)
        delay *= 2