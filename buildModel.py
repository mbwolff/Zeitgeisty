#!/usr/bin/env python3
"""
Copyright (c) 2022 Mark Wolff <wolff.mark.b@gmail.com>
Copying and distribution of this file, with or without modification, are
permitted in any medium without royalty provided the copyright notice and
this notice are preserved. This file is offered as-is, without any warranty.
"""

from utils import build_kw_dict, MySentences, MyDocs
from config import pickled_doc_dir, pickled_kw_dict_file, model_file, tweet_count, min_kw_count
from datetime import datetime
import pickle, spacy, os, time, logging, pprint, re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim.models import Word2Vec

sentences = MySentences(pickled_doc_dir)
model = Word2Vec(sentences ,workers=4)
model.save(model_file)

key_words = build_kw_dict(MyDocs(pickled_doc_dir), dict())

pickleFile = open(pickled_kw_dict_file, 'wb')
pickle.dump(key_words, pickleFile)
pickleFile.close()
