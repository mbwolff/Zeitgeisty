#!/usr/bin/env python3

from mastodon import Mastodon
from pprint import pprint
from bs4 import BeautifulSoup
import re
from mastodon_creds import my_access_token, my_client_id, my_client_secret, my_api_base_url

def get_id_from_last_set_of_docs():
    return 110829153646426700

def no_repeat(r, i):
    for p in r:
#        pprint(p)
        if p['id'] == i:
            return False
    return True

def find_new_min_id(r):
    min_id = 0
    for p in r:
        if p['id'] > min_id:
            min_id = p['id']
    return min_id

m = Mastodon(
#    client_id = 'YGVUFjJ5mkLwSsSHmE2vMhXhuyCFshfr_xUHJjVdTjg',
#    client_secret = 'wHIr0MaK41FqzL2W3TJtinO5peqUOPptMxv6zHCsL4Y',
#    api_base_url ='https://mastodon.social',
#    access_token = 'iy_26q5i4kSBZHnc_OtYuy0lMG5PQS7tNV7x9IAjfZA',
    client_id = my_client_id,
    client_secret = my_client_secret,
    api_base_url = my_api_base_url,
    access_token = my_access_token,
    ratelimit_method = 'pace'
)

results = []
latest = get_id_from_last_set_of_docs()

for tag in ['biden', 'maga']:
    tb = []
    
    batch = m.timeline_hashtag(tag, min_id=latest, limit=3)
    
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
    
pprint(results)
print('New min_id: ' + str(find_new_min_id(results)))