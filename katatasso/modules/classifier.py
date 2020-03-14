#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import juicer
import numpy as np
import pandas as pd

from katatasso.helpers.const import CATEGORIES
from katatasso.helpers.extraction import make_dictionary, process_dataframe, get_tfidf_counts
from katatasso.helpers.logger import rootLogger as logger
from katatasso.helpers.utils import load_model, load_y_test

try:
    from sklearn.metrics import accuracy_score
    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
except ModuleNotFoundError:
    logger.critical(f'Module scikit-learn not found. Please install before proceeding.')
    sys.exit(2)


def classify(text):
    """
    word vector counts
    """
    clf = load_model()
    y_test = load_y_test()
    dic = make_dictionary()

    features = []
    for word in dic:
        features.append(text.count(word[0]))
    predicted = clf.predict([features])
    logger.info(f'CLASSIFICATION => `{CATEGORIES[predicted[0]]}`')
    accuracy = accuracy_score([y_test[0]], predicted) * 100
    logger.info(f'     Accuracy: {accuracy  * 100}%')
    logger.info(f'     Accuracy: {np.mean(predicted == [y_test[0]]) * 100}%')
    return predicted[0], accuracy


def classifyv2(text):
    """
    tf-idf vectors
    """
    clf = load_model()
    y_test = load_y_test()
    counts = get_tfidf_counts(text)

    predicted = clf.predict(counts)
    logger.info(f'CLASSIFICATION => `{CATEGORIES[predicted[0]]}`')
    accuracy = accuracy_score(y_test.head(1), predicted) * 100
    logger.info(f'     Accuracy: {accuracy  * 100}%')
    logger.info(f'     Accuracy: {np.mean(predicted == y_test.head(1)) * 100}%')
    return predicted[0], accuracy
