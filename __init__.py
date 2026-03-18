#!/usr/bin/env python3
"""
Copyright (c) 2022 Mark Wolff <wolff.mark.b@gmail.com>
Copying and distribution of this file, with or without modification, are
permitted in any medium without royalty provided the copyright notice and
this notice are preserved. This file is offered as-is, without any warranty.
"""

from flask import Flask, render_template, url_for, request
from utils import modify_lemma, no_repeats, proofread, get_pos
from aphor import formulas
from config import pickled_kw_dict_file, model_file, common_words
import os, re, datetime, pickle, random, spacy
from gensim.models import Word2Vec

enc = 'utf-8'

app = Flask(__name__)

package_dir = os.path.dirname(os.path.abspath(__file__))

nlp = spacy.load("en_core_web_trf")
_model = Word2Vec.load(model_file)
word_vectors = _model.wv
del _model
vocab_len = len(word_vectors)
with open(pickled_kw_dict_file, 'rb') as f:
    model_keys = pickle.load(f)
aphor_dir = os.path.join(package_dir, "aphorisms")

def format_date(fname):
    date_time_str = fname.split("_")[0]
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
    return '{0:%d} {0:%B} {0:%Y}'.format(date_time_obj, "day", "month", "year")

@app.route("/")
def list_days(days=None):
    days = list()
    files = os.listdir(aphor_dir)
    files.sort(reverse=True)
    for fname in files:
        if fname.endswith('txt'):
            days.append([fname, format_date(fname)])
    return render_template('days.html', days=days)

@app.route("/query", methods=["POST"])
def query_aphorisms():
    query_text = request.form.get("query", "").strip()
    error = None
    aphorisms = []

    if query_text:
        doc = nlp(query_text)
        key_words = []
        for token in doc:
            if not token.is_stop and token.pos_ in {'PROPN', 'VERB', 'NOUN'} and token.lemma_ not in common_words:
                kw = (token.lemma_, token.pos_)
                if kw not in key_words and kw in model_keys:
                    key_words.append(kw)

        if not key_words:
            error = "No usable keywords found in your text. Try different words."
        else:
            used_words = []
            formula_keys = list(formulas.keys())
            for AAA in key_words:
                BBB = CCC = DDD = None
                category = random.choice(formula_keys)
                formula = random.choice(formulas[category])
                aphor = formula[0]
                no_terms = formula[1]
                aphor = aphor.replace('AAA', modify_lemma(AAA))

                bresult = word_vectors.most_similar(negative=[AAA[0]], topn=vocab_len)
                for b in list(reversed(bresult)):
                    for bpos in get_pos(b[0], model_keys):
                        if no_repeats([AAA, (b[0], bpos)], used_words):
                            BBB = (b[0], bpos)
                            used_words.append([AAA, BBB])
                            break
                    if BBB is not None:
                        break

                if BBB is not None:
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
                        if CCC is not None:
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
                                if DDD is not None:
                                    aphor = aphor.replace('DDD', modify_lemma(DDD))

                if not any(p in aphor for p in ['AAA', 'BBB', 'CCC', 'DDD']):
                    aphorisms.append(proofread(aphor))

    return render_template('query_results.html', query=query_text, aphorisms=aphorisms, error=error)


@app.route("/aphorisms/<fname>")
def display_aphorisms(fname):
    aphor_file = open(os.path.join(aphor_dir, fname), 'r', encoding=enc)
    stuff = aphor_file.readlines()
    aphorisms = list()
    for line in stuff:
        if not re.search('are the aphorisms', line) and re.search('\w', line):
            aphorisms.append(line)
    return render_template('aphorisms.html', aphorisms=[aphorisms, format_date(fname)])
