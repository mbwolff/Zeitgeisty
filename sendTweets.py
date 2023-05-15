#!/usr/bin/env python3
"""
Copyright (c) 2023 Mark Wolff <wolff.mark.b@gmail.com>
Copying and distribution of this file, with or without modification, are
permitted in any medium without royalty provided the copyright notice and
this notice are preserved. This file is offered as-is, without any warranty.
"""

# The file twitter_credsPost.py needs to be created in order to use tweepy
# and access Twitter.
from twitter_credsPost import consumer_key, consumer_secret, access_token, access_token_secret
from config import aphorisms_dir, package_dir
from time import localtime, sleep
import os, re, tweepy

#authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret)
#authenticate.set_access_token(access_token, access_token_secret)
#api = tweepy.API(authenticate, wait_on_rate_limit=True)

client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret
)

aphor_files = os.listdir(aphorisms_dir)
aphor_files.sort()
f = open(os.path.join(package_dir, 'aphorisms', aphor_files[-1]), 'r')
aphors = f.readlines()
f.close()

#start = time()
for aphor in aphors:
    r = localtime()
    if r.tm_hour == 3 and r.tm_min >= 15:
        break
    elif not re.search('are the aphorisms', aphor) and re.search('\w', aphor):
        aphor += "\nFor more Zeitgeisty Aphorisms visit https://zeitgeisty.hartwick.edu."
        response = client.create_tweet(text=aphor.rstrip())
        print(f"https://twitter.com/user/status/{response.data['id']}")
        sleep(1800) # wait 30 minutes