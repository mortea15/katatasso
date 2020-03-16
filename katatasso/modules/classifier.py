#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from katatasso.helpers.const import CATEGORIES
from katatasso.helpers.extraction import (get_tfidf_counts, make_dictionary,
                                          process_dataframe)
from katatasso.helpers.logger import rootLogger as logger
from katatasso.helpers.utils import load_model, load_y_test

try:
    from sklearn.metrics import accuracy_score
    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
    import juicer
    import numpy as np
    import pandas as pd
except ModuleNotFoundError as e:
    logger.critical(f'Module `{e.name}` not found. Please install before proceeding.')
    sys.exit(2)


def classify(text):
    """Classify the text using a Multinomial Naive Bayes model with
        word vector counts

        Parameters
        ----------
        text : str
            The text input to classify

        Returns
        -------
        category : int
            Predicted category for the text
        accuracy : float
            The accuracy classification score
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
    category = int(predicted[0])
    accuracy = float(accuracy)
    return category, accuracy


def classifyv2(text):
    """Classify the text using a Multinomial Naive Bayes model with
        TF-IDF (Term Frequency Inverse Document Frequency) vectors

        Parameters
        ----------
        text : str
            The text input to classify

        Returns
        -------
        category : int
            Predicted category for the text
        accuracy : float
            The accuracy classification score
    """
    clf = load_model()
    y_test = load_y_test()
    counts = get_tfidf_counts(text)

    predicted = clf.predict(counts)
    logger.info(f'CLASSIFICATION => `{CATEGORIES[predicted[0]]}`')
    accuracy = accuracy_score(y_test.head(1), predicted) * 100
    logger.info(f'     Accuracy: {accuracy  * 100}%')
    logger.info(f'     Accuracy: {np.mean(predicted == y_test.head(1)) * 100}%')
    category = int(predicted[0])
    accuracy = float(accuracy)
    return category, accuracy
