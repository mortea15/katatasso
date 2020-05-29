#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from katatasso.helpers.const import CATEGORIES
from katatasso.helpers.extraction import (get_tfidf_counts, make_dictionary,
                                          process_dataframe)
from katatasso.helpers.logger import rootLogger as logger
from katatasso.helpers.utils import load_model

try:
    from sklearn.metrics import accuracy_score
    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
    import juicer
    import numpy as np
    import pandas as pd
except ModuleNotFoundError as e:
    logger.critical(f'Module `{e.name}` not found. Please install before proceeding.')
    sys.exit(2)


def classify(text, algo='mnb'):
    """Classify the text using a Naive Bayes model with
        word vector counts

        Parameters
        ----------
        text : str
            The text input to classify

        algo : str
            The algorithm to use
            `mnb` for Multinomial Naïve Bayes,
            `cnb` for Complement Naïve Bayes

        Returns
        -------
        category : int
            Predicted category for the text
    """
    clf = load_model(version='v1', algo=algo)
    dic = make_dictionary()

    features = []
    for word in dic:
        features.append(text.count(word[0]))
    predicted = clf.predict([features])
    logger.info(f'CLASSIFICATION => `{CATEGORIES[predicted[0]]}`')
    category = int(predicted[0])
    return category


def classifyv2(text, algo='mnb'):
    """Classify the text using a Multinomial Naive Bayes model with
        TF-IDF (Term Frequency Inverse Document Frequency) vectors

        Parameters
        ----------
        text : str
            The text input to classify

        algo : str


        Returns
        -------
        category : int
            Predicted category for the text
    """
    clf = load_model(version='v2', algo=algo)
    counts = get_tfidf_counts(text, algo=algo)

    predicted = clf.predict(counts)
    logger.info(f'CLASSIFICATION => `{CATEGORIES[predicted[0]]}`')
    category = int(predicted[0])
    return category
