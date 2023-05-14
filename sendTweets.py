#!/usr/bin/env python3
"""
Copyright (c) 2023 Mark Wolff <wolff.mark.b@gmail.com>
Copying and distribution of this file, with or without modification, are
permitted in any medium without royalty provided the copyright notice and
this notice are preserved. This file is offered as-is, without any warranty.
"""

# The file twitter_creds.py needs to be created in order to use tweepy
# and access Twitter.
from twitter_creds import bearer_token, consumer_key, consumer_secret, access_token, access_token_secret
from config import aphorisms_dir, package_dir
import os, re, tweepy

aphor_files = os.listdir(aphorisms_dir)
aphor_files.sort()
f = open(os.path.join(package_dir, 'aphorisms', aphor_files[-1]), 'r')
aphors = f.readlines()
f.close()

for aphor in aphors:
    if not re.search('are the aphorisms', aphor) and re.search('\w', aphor):
        print(aphor.rstrip())