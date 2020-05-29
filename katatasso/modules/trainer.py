#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from datetime import datetime

from katatasso.helpers.const import FN_MODEL
from katatasso.helpers.extraction import (create_dataframe, make_dataset,
                                          make_dictionary, standardize,
                                          process_dataframe)
from katatasso.modules.metrics import learning_curve, measure
from katatasso.helpers.logger import rootLogger as logger
from katatasso.helpers.utils import save_model, load_model, save_obj, load_obj

try:
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split
    from sklearn.naive_bayes import MultinomialNB, ComplementNB
    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
    import matplotlib.pyplot as plt
except ModuleNotFoundError as e:
    logger.critical(f'Module `{e.name}` not found. Please install before proceeding.')
    sys.exit(2)


def generate_dataset():
    pass


def train(std=False, algo='mnb'):
    """Train a model using Naive Bayes with word vector counts

        Parameters
        ----------
        std : bool
            Standardize the data

        algo : str
            The algorithm to use. Can be either `mnb` or `cnb`

        Returns
        -------
    """
    dictionary = make_dictionary()
    features, labels = make_dataset(dictionary)
    ### Todo: Remove
    save_obj(features, 'v1_features.p')
    save_obj(labels, 'v1_labels.p')
    ###

    x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=69)
    
    if std:
        x_train, x_test = standardize(x_train, x_test)
    if algo == 'cnb':
        model = ComplementNB()
    elif algo == 'mnb':
        model = MultinomialNB()
    else:
        logger.critical(f'Parameter `algo` specifies unknown algorithm. Defaulting to `mnb`.')
        model = MultinomialNB()

    model.fit(x_train, y_train)
    save_model(model, version='v1', algo=algo)

    y_pred = model.predict(x_test)
    print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
    measure.evaluate(model, x_test, y_test)
    measure.performance_report(y_test, y_pred)
    measure.plot_confusion_mat(model, x_test, y_test)
    title = f'Learning Curves ({algo.upper()})'
    learning_curve.plot(model, x_test, y_test, title=title)


def trainv2(std=False, algo='mnb', n=None):
    """Train a model using Naive Bayes with TF-IDF (Term Frequency Inverse Document Frequency) vectors

        Parameters
        ----------
        std : bool
            Standardize the data.

        algo : str
            The algorithm to use. Can be either `mnb` or `cnb`
        
        n : int
            Select n samples from each category. (Default: All)

        Returns
        -------
    """
    df = create_dataframe(n=n)
    counts, df = process_dataframe(df, algo=algo)
    ### Todo: Remove
    save_obj(df, 'v2_dataframe.p')
    save_obj(counts, 'v2_counts.p')
    ###
    # messages_train, messages_test, labels_train, labels_test
    x_train, x_test, y_train, y_test = train_test_split(counts, df['label'], test_size=0.3, random_state=69)
    if std:
        x_train, x_test = standardize(x_train, x_test)
    if algo == 'cnb':
        model = ComplementNB()
    elif algo == 'mnb':
        model = MultinomialNB()
    else:
        logger.critical(f'Parameter `algo` specifies unknown algorithm. Defaulting to `mnb`.')
        model = MultinomialNB()

    model.fit(x_train, y_train)
    save_model(model, version='v2', algo=algo)

    y_pred = model.predict(x_test)
    
    print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
    measure.evaluate(model, x_test, y_test)
    measure.performance_report(y_test, y_pred)
    measure.plot_confusion_mat(model, x_test, y_test)
    title = f'Learning Curves ({algo.upper()})'
    learning_curve.plot(model, x_test, y_test, title=title)