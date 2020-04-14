#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

CATEGORIES = {
    -1: 'untagged',
    0: 'legitimate',
    1: 'spam',
    2: 'phishing',
    3: 'malware',
    4: 'fraud',
    5: 'unclassified'
}

FP_MODEL = os.getenv('CLF_MODEL_PATH', 'model.pkl')
CLF_DICT_NUM = int(os.getenv('CLF_DICT_NUM', 5000))
CLF_TRAININGDATA_PATH = os.getenv('CLF_TRAININGDATA_PATH', 'trainingdata/emails/')
DBFILE = 'tagger.db'