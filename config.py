#!/usr/bin/env python3
"""
Copyright (c) 2022 Mark Wolff <wolff.mark.b@gmail.com>
Copying and distribution of this file, with or without modification, are
permitted in any medium without royalty provided the copyright notice and
this notice are preserved. This file is offered as-is, without any warranty.
"""
import os

package_dir = os.path.dirname(os.path.abspath(__file__))

pickled_doc_dir = os.path.join(package_dir, "docs")
pickled_kw_dict_file = os.path.join(package_dir, "pickled_kws.pkl")
model_file = os.path.join(package_dir, "W2Vmodel")
aphorisms_dir = os.path.join(package_dir, "aphorisms")

tweet_count = 10
min_kw_count = 5
common_words = ["day", "time", "say", "break", "#", "get", "year", "thing",
    "people", "know", "agree", "think", "take", "go", "tell", "work", "end",
    "want", "need", "today", "question", "play", "stop", "watch", "-", "ask",
    "state", "look", "help", "%", "see", "try", "account", "come", ".",
    "up", "f", "/", "amp", "&", "miss", "down", "'", "way", "\"", '+', '!',
    "man", "case", ":", "put", "word", "week", "month", "in", ",", "\(", "\)",
    "_"]
odd_verbs = ['plan', 'shit', 'slap', 'ship', 'spin', 'compel', 'refer', 'upset',
    'snub', 'forget', 'strip', 'commit', 'swim', 'admit']
keep_final_e_verbs = ['toe', 'coe', 'Coe', 'be']
determined_proper_nouns = ['Yankees', 'Republicans', 'Democrats', 'Senate',
    'Pope', 'Committee', 'iPhone____14', 'Supreme____Court',
    'Prime____Minister', 'U.S.', 'House', 'USA', 'GOP', 'Capitol', 'NFL',
    'MLB', 'AL', 'NL', 'NBA', 'West']
