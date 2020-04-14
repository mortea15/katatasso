#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from katatasso.helpers.const import FP_MODEL
from katatasso.helpers.extraction import (create_dataframe, make_dataset,
                                          make_dictionary, normalize,
                                          process_dataframe)
from katatasso.helpers.logger import rootLogger as logger
from katatasso.helpers.utils import save_model, save_y_test

try:
    from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
    from sklearn.model_selection import train_test_split as TTS
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
    from diffprivlib.models import GaussianNB as PrivateNB
    import numpy as np
except ModuleNotFoundError as e:
    logger.critical(f'Module `{e.name}` not found. Please install before proceeding.')
    sys.exit(2)


def train(norm=False, privacy=False):
    """Train a model using Multinomial Naive Bayes with word vector counts

        Parameters
        ----------
        norm : bool
            Whether to normalize the data.
        privacy : bool
            Whether to use a differentially private Naive Bayes classifier.

        Returns
        -------
    """
    dictionary = make_dictionary()
    features, labels = make_dataset(dictionary)

    x_train, x_test, y_train, y_test = TTS(features, labels, test_size=0.3)
    if norm:
        x_train, x_test = normalize(x_train, x_test)

    if privacy:
        model = PrivateNB(epsilon=0.5)
    else:
        model = MultinomialNB()
    model.fit(x_train, y_train)

    predicted = model.predict(x_test)
    print(f'Accuracy: {accuracy_score(y_test, predicted) * 100}%')
    logger.debug(f'     Accuracy: {np.mean(predicted == y_test) * 100}%')
    logger.debug(f'     Confusion Matrix:\n{confusion_matrix(y_test, predicted)}')
    logger.debug(classification_report(y_test, predicted, zero_division=1))
    save_model(model)
    save_y_test(y_test)


def trainv2(norm=False, privacy=False):
    """Train a model using Multinomial Naive Bayes with TF-IDF (Term Frequency Inverse Document Frequency) vectors

        Parameters
        ----------
        norm : bool
            Whether to normalize the data.
        privacy : bool
            Whether to use a differentially private naive Bayes classifier.

        Returns
        -------
    """
    df = create_dataframe()
    counts, df = process_dataframe(df)
    # messages_train, messages_test, labels_train, labels_test
    x_train, x_test, y_train, y_test = TTS(counts, df['label'], test_size=0.3)
    if norm:
        x_train, x_test = normalize(x_train, x_test)
    if privacy:
        model = PrivateNB(epsilon=0.5)
    else:
        model = MultinomialNB()
    model.fit(x_train, y_train)

    predicted = model.predict(x_test)
    print(f'Accuracy (SKLEARN): {accuracy_score(y_test, predicted) * 100}%')
    print(f'Accuracy (NUMPY): {np.mean(predicted == y_test) * 100}%')
    print(confusion_matrix(y_test, predicted))
    print(classification_report(y_test, predicted, zero_division=1))
    save_model(model)
    save_y_test(y_test)
