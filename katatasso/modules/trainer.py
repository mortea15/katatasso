#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import numpy as np

from katatasso.helpers.const import FP_MODEL
from katatasso.helpers.extraction import (create_dataframe, make_dataset,
                                          make_dictionary, process_dataframe)
from katatasso.helpers.logger import rootLogger as logger
from katatasso.helpers.utils import save_model

try:
    from sklearn.metrics import accuracy_score, confusion_matrix
    from sklearn.model_selection import train_test_split as TTS
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
except ModuleNotFoundError:
    logger.error(f'Module scikit-learn not found. Please install before proceeding.')
    sys.exit(2)


def trainv2():
    df = create_dataframe()
    counts, df = process_dataframe(df)

    x_train, x_test, y_train, y_test = TTS(counts, df['label'], test_size=0.3)
    model = MultinomialNB().fit(x_train, y_train)
    predicted = model.predict(x_test)
    print(f'{accuracy_score(y_test, predicted) * 100}%')
    print(f'{np.mean(predicted == y_test) * 100}%')
    logger.debug(f'Confusion Matrix:\n{confusion_matrix(y_test, predicted)}')
    save_model(model, FP_MODEL)


def train():
    dictionary = make_dictionary()
    features, labels = make_dataset(dictionary)

    x_train, x_test, y_train, y_test = TTS(features, labels, test_size=0.3)

    model = MultinomialNB()
    model.fit(x_train, y_train)

    predicted = model.predict(x_test)
    print(f'{accuracy_score(y_test, predicted) * 100}%')
    print(f'{np.mean(predicted == y_test) * 100}%')
    logger.debug(f'Confusion Matrix:\n{confusion_matrix(y_test, predicted)}')
    save_model(model, FP_MODEL)
