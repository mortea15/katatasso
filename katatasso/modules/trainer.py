#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import sqlite3

from katatasso.helpers.const import CATEGORIES, FP_MODEL, DBFILE, CLF_TRAININGDATA_PATH
from katatasso.helpers.extraction import get_file_paths, make_dictionary
from katatasso.helpers.logger import rootLogger as logger
from katatasso.helpers.utils import progress_bar, save_model

try:
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split as TTS
    from sklearn.naive_bayes import MultinomialNB
except ModuleNotFoundError:
    logger.error(f'Module scikit-learn not found. Please install before proceeding.')
    sys.exit(2)


# Create a data set for the classification
def make_dataset(dictionary):
    file_paths = get_file_paths()
    features = []
    labels = []
    logger.info(f'Creating dataset from {len(file_paths)} files')
    for fp in progress_bar(file_paths):
        data = []
        with open(fp, encoding='latin-1') as f:
            words = f.read().split()
        for entry in dictionary:
            data.append(words.count(entry[0]))
        features.append(data)

        if 'legit' in fp:
            tag = 0
        elif 'spam' in fp:
            tag = 1
        elif 'phishing' in fp:
            tag = 2
        elif 'malware' in fp:
            tag = 3
        elif 'fraud' in fp:
            tag = 4
        else:
            tag = 5
        
        labels.append(tag)
        
    return features, labels


def train():
    dictionary = make_dictionary()
    features, labels = make_dataset(dictionary)

    x_train, x_test, y_train, y_test = TTS(features, labels, test_size=0.3)

    clf = MultinomialNB()
    clf.fit(x_train, y_train)

    preds = clf.predict(x_test)
    logger.info(f'Accuracy Score: {accuracy_score(y_test, preds)}')
    save_model(clf, FP_MODEL)
