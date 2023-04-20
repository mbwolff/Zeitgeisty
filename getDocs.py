#!/usr/bin/env python3
"""
Copyright (c) 2022 Mark Wolff <wolff.mark.b@gmail.com>
Copying and distribution of this file, with or without modification, are
permitted in any medium without royalty provided the copyright notice and
this notice are preserved. This file is offered as-is, without any warranty.
"""

from utils import build_kw_dict, parse
from config import pickled_doc_dir, tweet_count, min_kw_count

# The file twitter_creds.py needs to be created in order to use tweepy
# and access Twitter.
from twitter_creds import bearer_token, consumer_key, consumer_secret, access_token, access_token_secret

from pygooglenews import GoogleNews
from datetime import datetime
import pickle, spacy, os, tweepy, time, re, pprint

os.chdir(os.path.dirname(os.path.abspath(__file__)))

date_time = datetime.fromtimestamp(time.time())
str_date_time = date_time.strftime("%Y-%m-%d_%H-%M-%S")
os.environ["TOKENIZERS_PARALLELISM"] = "true"
if not os.path.exists(pickled_doc_dir):
    os.makedirs(pickled_doc_dir)

gn = GoogleNews()
top = gn.top_news()

entries = top["entries"]
headlines = list()
for entry in entries:
  if len(headlines) > 0 and headlines[-1]['text'].startswith(entry['title']):
    headlines[-1]['text'] = entry['title']
    headlines[-1]['source'] = entry['link']
  else:
    headlines.append({ 'text': entry['title'], 'source': entry['link'] })
  if entry.sub_articles:
    for sub_art in entry.sub_articles:
      if headlines[-1]['text'].startswith(sub_art['title']):
        headlines[-1]['text'] = sub_art['title']
        headlines[-1]['source'] = sub_art['url']
      else:
        headlines.append({ 'text': sub_art['title'], 'source': sub_art['url'] })

parsed_headlines = parse(headlines)

authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret)
authenticate.set_access_token(access_token, access_token_secret)
api = tweepy.API(authenticate, wait_on_rate_limit = True)

kw_dict = build_kw_dict([ doc['parsed'] for doc in parsed_headlines ], dict())

tweets = list()
for kw, val in sorted(kw_dict.items(), key=lambda e: e[1], reverse=True):
    print(kw[0] + ': ' + str(val))
    if val < min_kw_count:
        continue
    results = [
        { 'text': tweet.full_text, 'source': tweet.id } for tweet in tweepy.Cursor(
            api.search_tweets,
            q=kw[0] + ' -filter:retweets',
            lang='en',
            result_type="mixed",
            tweet_mode="extended"
        ).items(tweet_count)]
    tweets.extend(results)

parsed_docs = parsed_headlines + parse(tweets)
pprint.pprint(parsed_docs)

pickleFile = open(os.path.join(pickled_doc_dir, str_date_time + '_docs.pkl'), 'wb')
pickle.dump(parsed_docs, pickleFile)
pickleFile.close()
