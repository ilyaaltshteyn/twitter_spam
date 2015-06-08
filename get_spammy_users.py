# This script looks for tweets about etsy and ebay, then runs a spam detector on
# them, then writes them to a file.
import tweetPreprocessor
from pymongo import MongoClient
import time
import math
from random import random

# Establish mongo info:
client = MongoClient()
db = client.tweets
collect = db.random_sample_june7th
found = collect.find()

