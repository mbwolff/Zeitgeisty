#!/usr/bin/env python3
"""
Copyright (c) 2023 Mark Wolff <wolff.mark.b@gmail.com>
Copying and distribution of this file, with or without modification, are
permitted in any medium without royalty provided the copyright notice and
this notice are preserved. This file is offered as-is, without any warranty.
"""

from utils import parse
from config import pickled_doc_dir, tweet_count, min_kw_count

import pickle, spacy, os

docsDir = '/home/mark/Zeitgeisty/docs'

for fname in os.listdir(docsDir):
    if fname.endswith('pkl'):
        file = os.path.join(docsDir, fname)
        print(file)
        pickleIn = open(file, 'rb')
        docs = parse(pickle.load(pickleIn))
        pickleIn.close()
        pickleOut = open(file, 'wb')
        pickle.dump(docs, pickleOut)
        pickleOut.close()