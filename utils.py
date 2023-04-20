#!/usr/bin/env python3
"""
Copyright (c) 2022 Mark Wolff <wolff.mark.b@gmail.com>
Copying and distribution of this file, with or without modification, are
permitted in any medium without royalty provided the copyright notice and
this notice are preserved. This file is offered as-is, without any warranty.
"""

from gensim.models.phrases import Phrases, ENGLISH_CONNECTOR_WORDS
from config import common_words, odd_verbs, keep_final_e_verbs, determined_proper_nouns
from pronouncing import phones_for_word, stresses
import re, pprint, spacy, os, pickle

nlp = spacy.load("en_core_web_trf")
cvc = re.compile(r"([^aeiou])([aeiou])([^aeiouxy])$")

def get_pos(token, model_keys):
    hits = list()
    for pos in ['PROPN', 'VERB', 'NOUN']:
        if (token, pos) in model_keys:
            hits.append([token, pos, model_keys[(token, pos)]])
    results = sorted(hits, key = lambda x: x[2], reverse=True)
    return [ r[1] for r in results ]

def proofread(aphorism):
    tokens = nlp(aphorism)
    new_tokens = list()
    plural_y = re.compile(r"([^aeiou])ys\b")
    for i in range(len(tokens)):
        text = tokens[i].text
        if plural_y.match(tokens[i].text) and tokens[i].lemma_.endswith("y"):
            text = plural_y.sub(r"\1ies", text)

        if i == 0:
            new_tokens.append(text)
        elif tokens[i-1].tag_ in ['NNS', 'NNPS'] and tokens[i].tag_ == 'VBZ':
            if tokens[i].lemma_ == 'be':
                new_tokens.append('are')
            else:
                new_tokens.append(tokens[i].lemma_)
        elif tokens[i-1].text == 'no' and tokens[i].tag_ == 'DT':
            continue
        elif tokens[i-1].text == 'ca' and tokens[i].text == 'n\'t':
            new_tokens[-1] = 'can\'t'
        elif tokens[i-1].text == 'can' and tokens[i].text == 'not':
            new_tokens[-1] = 'cannot'
        elif tokens[i-1].text == 'does' and tokens[i].text == 'n\'t':
            new_tokens[-1] = 'doesn\'t'
        elif tokens[i-1].text == 'wo' and tokens[i].text == 'n\'t':
            new_tokens[-1] = 'won\'t'
        elif tokens[i-1].text == 'would' and tokens[i].text == 'n\'t':
            new_tokens[-1] = 'wouldn\'t'
        elif tokens[i-1].text == 'could' and tokens[i].text == 'n\'t':
            new_tokens[-1] = 'couldn\'t'
        elif tokens[i-1].text == 'should' and tokens[i].text == 'n\'t':
            new_tokens[-1] = 'shouldn\'t'
        else:
            new_tokens.append(text)
    string = ' '.join(new_tokens)
    string = re.sub(r" ([\'?!.,:;\-]+)", r"\1", string)
    string = re.sub(r"\- ", r"-", string)
    return string[0].upper() + string[1:]

def no_repeats(words, used_words):
    words.sort()
    for group in used_words:
        group.sort()
        if words == group:
            return False
    for word in words[:-1]:
        if word[0].lower() in words[-1][0].lower() or words[-1][0].lower() in word[0].lower():
            return False
    return True

def count_words(aphorisms):
    no_words = 0
    for aphor in aphorisms:
        no_words = no_words + len(aphor.split())
    return no_words

def modify_lemma(tup):
    string = tup[0]
    pos = tup[1]
    if pos == 'VERB':
        if string.endswith("ing") or string in keep_final_e_verbs:
            string = string + "ing"
        elif string in odd_verbs:
            string = re.sub(r"([aeiou])([^aeiouy])$", r"\1\2\2ing", string)
        elif cvc.match(string) and stresses(phones_for_word(string)[0])[-1] == '1':
            string = cvc.sub(r"\1\2\3\3ing", string)
        else:
            string = re.sub(r"^([dltv])ie$", r"\1y", string)
            string = re.sub(r"____be$", "____being", string)
            string = re.sub(r"(?!ing$)ee$", r"eeing", string)
            string = re.sub(r"(?!ing$)oo([^aeiou])$", r"oo\1ing", string)
            string = re.sub(r"(?!ing$)ee([^aeiou])$", r"ee\1ing", string)
            string = re.sub(r"(?!ing$)e*$", r"ing", string)
            string = re.sub("inging$", "ing", string)
    elif pos == 'PROPN':
        if string in determined_proper_nouns:
            string = 'the____' + string
    string = string.replace('____', ' ')
    string = string.replace('HASHTAG__', '#')
    return string

def build_kw_dict(docs, kw_dict):
    for doc in docs:
        for token in doc:
            if not token.is_stop and token.pos_ in {'PROPN', 'VERB', 'NOUN'} and token.lemma_ not in common_words:
                this_tuple = (token.lemma_, token.pos_)
                if this_tuple in kw_dict:
                    kw_dict[this_tuple] = kw_dict[this_tuple] + 1
                else:
                    kw_dict[this_tuple] = 1
    return kw_dict

def parse(docs):
    parsed_docs = [ nlp(doc['text']) for doc in docs ]
    preprocessed_docs = list()
    for parsed_doc in parsed_docs:
        ppd = list()
        for idx in range(len(parsed_doc)):
#        for token in parsed_doc:
            token = parsed_doc[idx]
            string = token.text
            if string == '#':
                idx += 1
                string = string + parsed_doc[idx].text
#            if string == '#':
#                string = 'MarkMark'
            if token.pos_ not in { 'PROPN' }:
                string = string.lower()
            if token.pos_ not in { 'PUNCT' }:
                ppd.append(string)
        preprocessed_docs.append(ppd)

    bigram_transformer = Phrases(preprocessed_docs, min_count=3, threshold=0.5,
                                 delimiter='____', scoring="npmi",
                                 connector_words=ENGLISH_CONNECTOR_WORDS)
    bigrams = bigram_transformer[preprocessed_docs]

    trigram_transformer = Phrases(bigrams, min_count=3, threshold=0.5,
                                 delimiter='____', scoring="npmi",
                                 connector_words=ENGLISH_CONNECTOR_WORDS)
    trigrams = trigram_transformer[bigrams]

    for idx in range(len(docs)):
        text = docs[idx]['text']
        for token in trigrams[idx]:
            if token != None and '____' in token:
#                string = token.replace('MarkMark____', '#')
                string = token.replace('____', ' ')
                text = text.replace(string, token)
        docs[idx]['parsed'] = nlp(text) # with POS tags

    return docs

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            if fname.endswith('pkl'):
                pickleFile = open(os.path.join(self.dirname, fname), 'rb')
                docs = pickle.load(pickleFile)
                for sent in [ doc['parsed'] for doc in docs ]:
#                    lemmas = list()
#                    for idx in range(len(sent)-1):
#                        if sent[idx].lemma_ == '#':
#                            lemmas.append('HASHTAG__' + sent[idx+1].lemma_)
#                            idx += 1
#                        else:
#                            lemmas.append(sent[idx].lemma_)
#                    yield lemmas
                    yield [ token.lemma_ for token in sent ]

class MyDocs(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        headlines = tweets = 0
        for fname in os.listdir(self.dirname):
            if fname.endswith('pkl'):
                pickleFile = open(os.path.join(self.dirname, fname), 'rb')
                docs = pickle.load(pickleFile)
                for source in [ doc['source'] for doc in docs ]:
                    if "http" in str(source):
                        headlines = headlines + 1
                    else:
                        tweets = tweets + 1
                for sent in [ doc['parsed'] for doc in docs ]:
#                    limit = len(sent) - 1
#                    for idx in range(limit):
#                        if sent[idx].lemma_ == '#':
##                            sent[idx+1].text = 'HASHTAG__' + sent[idx+1].text
#                            sent[idx+1].lemma_ = 'HASHTAG__' + sent[idx+1].lemma_
#                            sent.pop(idx)
#                            idx -= 1
                    yield sent
        print("Headlines: " + str(headlines) + ", Tweets: " + str(tweets))
