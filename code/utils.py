#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2018 - songheqi <songheqi1996@gmail.com>

from sklearn.metrics import confusion_matrix
import numpy as np

def parse_data(filename):
    with open(filename, 'r+') as f:
        data = []
        new_sen = []
        for line in f.readlines():
            line = line.strip()
            if line and len(line) != 0:
                new_sen.append(line.split(' '))
            else:
                if new_sen:
                    data.append(new_sen)
                new_sen = []
    f.close()
    
    return data


def show_data():
    pass