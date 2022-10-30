#!/usr/bin/env python3
"""
Copyright (c) 2022 Mark Wolff <wolff.mark.b@gmail.com>
Copying and distribution of this file, with or without modification, are
permitted in any medium without royalty provided the copyright notice and
this notice are preserved. This file is offered as-is, without any warranty.
"""

from utils import build_kw_dict, modify_lemma, count_words, no_repeats, proofread, get_pos
from aphor import formulas
from config import pickled_doc_dir, pickled_kw_dict_file, model_file, tweet_count, min_kw_count, common_words, aphorisms_dir

import pickle, spacy, os, pprint, random, time
from gensim.models import Word2Vec
from datetime import datetime

os.chdir(os.path.dirname(os.path.abspath(__file__)))

model = Word2Vec.load(model_file)
word_vectors = model.wv
del model

vocab_len = len(word_vectors)

doc_files = os.listdir(pickled_doc_dir)
doc_files.sort()
pickleFile = open(os.path.join(pickled_doc_dir, doc_files[-1]), 'rb')
latest_docs = pickle.load(pickleFile)
pickleFile.close()

docs_dict = build_kw_dict([ doc['parsed'] for doc in latest_docs ], dict())

key_words = list()
for kw, val in sorted(docs_dict.items(), key=lambda e: e[1], reverse=True):
    if kw[0] in common_words:
        continue
    if val >= min_kw_count:
        key_words.append(kw)
for kw in key_words:
    print(kw)

pickleFile = open(pickled_kw_dict_file, 'rb')
model_keys = pickle.load(pickleFile)
pickleFile.close()

aphorisms = list()
total_words = 0
formula_keys = list(formulas.keys())
used_words = []
while total_words < 1667:
    for i in range(len(key_words)):
        AAA = BBB = CCC = DDD = None
        apos = bpos = cpos = dpos = None
        total_words = count_words(aphorisms)
        if total_words >= 1667:
            break
        else:
            AAA = key_words[i]
            category = random.choice(formula_keys)
            formula = random.choice(formulas[category])
            aphor = formula[0]
            no_terms = formula[1]
            aphor = aphor.replace('AAA', modify_lemma(AAA))
            bresult = word_vectors.most_similar(negative=[AAA[0]], topn=vocab_len)
            for b in list(reversed(bresult)):
                for bpos in get_pos(b[0], model_keys): # return list of pos
                    if no_repeats([AAA, (b[0], bpos)], used_words):
                        BBB = (b[0], bpos)
                        used_words.append([AAA, BBB])
                        break
                if BBB is not None:
                    break
            if BBB != "":
                aphor = aphor.replace('BBB', modify_lemma(BBB))
                if no_terms >= 3:
                    cresult = word_vectors.most_similar(positive=[BBB[0]], negative=[AAA[0]], topn=vocab_len)
                    for c in cresult:
                        for cpos in get_pos(c[0], model_keys):
                            if no_repeats([AAA, BBB, (c[0], cpos)], used_words):
                                CCC = (c[0], cpos)
                                used_words.append([AAA, BBB, CCC])
                                break
                        if CCC is not None:
                            break
                    if CCC != "":
                        aphor = aphor.replace('CCC', modify_lemma(CCC))
                        if no_terms == 4:
                            dresult = word_vectors.most_similar(positive=[BBB[0]], negative=[AAA[0], CCC[0]], topn=vocab_len)
                            for d in list(reversed(dresult)):
                                for dpos in get_pos(d[0], model_keys):
                                    if no_repeats([AAA, BBB, CCC, (d[0], dpos)], used_words):
                                        DDD = (d[0], dpos)
                                        used_words.append([AAA, BBB, CCC, DDD])
                                        break
                                if DDD is not None:
                                    break
                            if DDD != "":
                                aphor = aphor.replace('DDD', modify_lemma(DDD))
            if "AAA" in aphor or "BBB" in aphor or "CCC" in aphor or "DDD" in aphor:
                print("There was a problem with: " + aphor)
                print("AAA was: " + AAA)
            else:
                aphorisms.append(proofread(aphor))

else:
    date_time = datetime.fromtimestamp(time.time())
    str_date_time = date_time.strftime("%Y-%m-%d_%H-%M-%S")
    with open(os.path.join(aphorisms_dir, str_date_time + '_aphorisms.txt'), 'w') as f:
        print("Here are the aphorisms from " + str(date_time) + "\n", file=f)
        for aphor in aphorisms:
            print(aphor, file=f)
