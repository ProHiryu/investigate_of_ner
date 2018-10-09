#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2018 - songheqi <songheqi1996@gmail.com>

from stanfordcorenlp import StanfordCoreNLP
import numpy as np
from utils import *

import logging
from tqdm import tqdm
import pickle


nlp = StanfordCoreNLP(r'../stanford-corenlp-full-2018-10-05', lang='zh', memory='8g')

def simple_test():

    # nlp = StanfordCoreNLP(r'../stanford-corenlp-full-2016-10-31/', lang='zh', quiet=False, logging_level=logging.DEBUG)
    # sentence = 'Guangdong University of Foreign Studies (GDUFS) is located in Guangzhou.'
    sentence = '帮我订一张明天上午到深圳的机票'
    print(nlp.ner(sentence))


def futher_test(need_parse=True, filename='corpus/example.test'):

    if need_parse:
        data = parse_data(filename)
        X = []
        labels = []
        sentence = ''
        for sentence_split in data:
            for c, y in sentence_split:
                sentence += c
                labels.append(y)
            X.append(sentence)
            sentence = ''
        
        with open('X', 'wb') as f:
            pickle.dump(X, f)
        f.close()

        with open('labels', 'wb') as f:
            pickle.dump(labels, f)
        f.close()

        # print(X[0], labels[:10])

        pred = []
        for sentence in tqdm(X, ascii=True, desc="Getting NER..."):
            for y_hat in nlp.ner(sentence):
                pred.append(y_hat[1])
        
        with open('pred', 'wb') as f:
            pickle.dump(pred, f)
        f.close()
    else:
        with open('pred', 'rb') as f:
            pred = pickle.load(f)
        f.close()

        with open('labels', 'rb') as f:
            labels = pickle.load(f)
        f.close()

        with open('X', 'rb') as f:
            X = pickle.load(f)
        f.close()
    
    lenx = 0
    for x in X:
        lenx += len(x)
    print(len(pred),len(labels),lenx)
    print(pred[-20:], labels[-20:])

    print(nlp.pos_tag(X[-1]))
    print(nlp.ner(X[-1]), x)

    show_data()


def single_step(sentence):
    return nlp.ner(sentence)


def custom_test(filename='corpus/test'):
    with open(filename, 'r') as f:
        lines = f.readlines()
        with open('out', 'w') as fout:
            for sentence in lines:
                fout.write(str(nlp.ner(sentence)) + '\n')
            fout.close()
        f.close()

custom_test()
nlp.close()