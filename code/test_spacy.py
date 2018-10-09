#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2018 - songheqi <songheqi1996@gmail.com>

import spacy

import zh_core_web_sm

nlp = spacy.load('zh')

def simple_test():
    doc = nlp("帮我订一张明天上午到深圳的机票")
    for token in doc:
        print(token.text, token.ent_iob_, token.ent_type_)

def single_step(sentence):
    return nlp(sentence)


def custom_test(filename='corpus/test'):
    with open(filename, 'r') as f:
        lines = f.readlines()
        with open('out_spacy', 'w') as fout:
            for sentence in lines:
                pred = []
                doc = single_step(sentence)
                for token in doc:
                    pred.append((token.text, token.ent_type_))
                fout.write(str(pred) + '\n')
                pred = []
            fout.close()
        f.close()

custom_test()