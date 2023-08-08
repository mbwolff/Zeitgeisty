#!/usr/bin/env python3
"""
Copyright (c) 2023 Mark Wolff <wolff.mark.b@gmail.com>
Copying and distribution of this file, with or without modification, are
permitted in any medium without royalty provided the copyright notice and
this notice are preserved. This file is offered as-is, without any warranty.
"""

"""
mastodon = Mastodon(client_id = 'YGVUFjJ5mkLwSsSHmE2vMhXhuyCFshfr_xUHJjVdTjg', client_secret = 'wHIr0MaK41FqzL2W3TJtinO5peqUOPptMxv6zHCsL4Y', api_base_url ='https://mastodon.social', access_token = 'iy_26q5i4kSBZHnc_OtYuy0lMG5PQS7tNV7x9IAjfZA', ratelimit_method = 'pace')

In Twitter version we retrieve source and text, and with the text we generate parsed.
The fields in Mastodon are 'url' for source and 'content' for text. We will need to strip HTML tags from content (usually <p>, <a>, <span>)
"""

from utils import build_kw_dict, parse
from config import pickled_doc_dir, tweet_count, min_kw_count
from mastodon import Mastodon
from pprint import pprint
from bs4 import BeautifulSoup

# The file twitter_creds.py needs to be created in order to use tweepy
# and access Twitter.
#from twitter_creds import bearer_token, consumer_key, consumer_secret, access_token, access_token_secret
from mastodon_creds import my_access_token, my_client_id, my_client_secret, my_api_base_url
from pygooglenews import GoogleNews
from datetime import datetime
import pickle, spacy, os, tweepy, time, re, pprint

def get_id_from_last_set_of_docs():
    doc_files = os.listdir(pickled_doc_dir)
    doc_files.sort()
    pickleFile = open(os.path.join(pickled_doc_dir, doc_files[-1]), 'rb')
    latest_docs = pickle.load(pickleFile)
    pickleFile.close()
    
    return 110829153646426700
#    return find_new_min_id(latest_docs)

def no_repeat(r, i):
    for p in r:
#        pprint(p)
        if p['id'] == i:
            return False
    return True

def find_new_min_id(r):
    min_id = 0
    for p in [x for x in r if x['source'] == 'Mastodon']:
        if p['id'] > min_id:
            min_id = p['id']
    return min_id


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

#authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret)
#authenticate.set_access_token(access_token, access_token_secret)
#api = tweepy.API(authenticate, wait_on_rate_limit = True)
m = Mastodon(
    client_id = my_client_id,
    client_secret = my_client_secret,
    api_base_url = my_api_base_url,
    access_token = my_access_token,
    ratelimit_method = 'pace'
)
latest = get_id_from_last_set_of_docs()

kw_dict = build_kw_dict([ doc['parsed'] for doc in parsed_headlines ], dict())

results = list()
for kw, val in sorted(kw_dict.items(), key=lambda e: e[1], reverse=True):
    print(kw[0] + ': ' + str(val))
    if val < min_kw_count:
        continue
#    results = [
 #       { 'text': tweet.full_text, 'source': tweet.id } for tweet in tweepy.Cursor(
 #           api.search_tweets,
#            q=kw[0] + ' -filter:retweets',
#            lang='en',
#            result_type="mixed",
#            tweet_mode="extended"
#        ).items(tweet_count)]
#    toots.extend(results)
    tb = list()
    batch = m.timeline_hashtag(kw[0], min_id=latest, limit=3)
    while batch:
        if len(tb) >= 10:
            break
        else:
            batch = m.fetch_next(batch)
            for s in batch:
#                pprint(s)
                if s['language'] == 'en' and no_repeat(results, s['id']):
                    string = BeautifulSoup(s['content'], "html.parser").text
                    string = re.sub('https*://[\.\w/\-]+', '', string)
                    tb.append({ 'source': 'Mastodon',
                                'id': s['id'],
                                'text': string })
    results = results + tb

parsed_docs = parsed_headlines + parse(results)
pprint(parsed_docs)

pickleFile = open(os.path.join(pickled_doc_dir, str_date_time + '_docs.pkl'), 'wb')
pickle.dump(parsed_docs, pickleFile)
pickleFile.close()
