#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import sys

import emailyzer

from katatasso.helpers.const import (CATEGORIES, CLF_TRAININGDATA_PATH, DBFILE,
                                     FP_MODEL)
from katatasso.helpers.extraction import (get_all_tags, get_file_paths,
                                          make_dictionary)
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
    features = []
    labels = []
    tags = get_all_tags()
    if tags:
        logger.info(f'Creating dataset from {len(tags)} files')
        for filename, tag in progress_bar(tags):
            filepath = CLF_TRAININGDATA_PATH + filename
            data = []
            email = emailyzer.from_file(filepath)
            words = email.html_as_text.split()

            for entry in dictionary:
                data.append(words.count(entry[0]))
            features.append(data)
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
