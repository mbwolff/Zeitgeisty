#!/usr/bin/env python3
"""
Copyright (c) 2023 Mark Wolff <wolff.mark.b@gmail.com>
Copying and distribution of this file, with or without modification, are
permitted in any medium without royalty provided the copyright notice and
this notice are preserved. This file is offered as-is, without any warranty.
"""

# The file twitter_credsPost.py needs to be created in order to use tweepy
# and access Twitter.
#from twitter_credsPost import consumer_key, consumer_secret, access_token, access_token_secret
from mastodon import Mastodon
from threads_api.src.threads_api import ThreadsAPI
import asyncio
from mastodon_creds import my_access_token, my_client_id, my_client_secret, my_api_base_url, instagram_username, instagram_password
from config import aphorisms_dir, package_dir
from time import localtime, sleep
import os, re

async def post2threads(aphor):
    api = ThreadsAPI()
    
    await api.login(instagram_username, instagram_password, cached_token_path=".token")
    result = await api.post(caption=aphor)

#    if result:
#        print("Post has been successfully posted")
#    else:
#        print("Unable to post.")
    await api.close_gracefully()

#authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret)
#authenticate.set_access_token(access_token, access_token_secret)
#api = tweepy.API(authenticate, wait_on_rate_limit=True)

#client = tweepy.Client(
#    consumer_key=consumer_key, consumer_secret=consumer_secret,
#    access_token=access_token, access_token_secret=access_token_secret
#)

async def main():
    m = Mastodon(
        client_id = my_client_id,
        client_secret = my_client_secret,
        api_base_url = my_api_base_url,
        access_token = my_access_token,
        ratelimit_method = 'pace'
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
            try:
                aphor = re.sub('#\s+', '#', aphor)
    #            aphor += "\nFor more Zeitgeisty Aphorisms visit https://zeitgeisty.hartwick.edu."
                m.status_post(aphor)
                post2threads(aphor)
    #            response = client.create_tweet(text=aphor.rstrip())
    #            print(f"https://twitter.com/user/status/{response.data['id']}")
                sleep(1800) # wait 30 minutes
            except Exception:
                pass

asyncio.run(main())