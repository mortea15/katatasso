#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import sys

import tqdm

from katatasso.helpers.logger import rootLogger as logger


def prepare_result(output):
    # TODO Convert to JSON if json
    result = output
    return result


def progress_bar(it):
    if logger.level < 30:
        return tqdm.tqdm(it)
    else:
        return it

# Save the classifier
def save_model(clf, name):
    try:
        with open(name, 'wb') as f:
            pickle.dump(clf, f)
        logger.info(f'Pickled model saved to {name}')
    except Exception as e:
        logger.warn('An unexpected error occurred while saving the model.')
        logger.error(e)

# Load the classifier
def load_model(clf_path):
    try:
        with open(clf_path, 'rb') as f:
            clf = pickle.load(f, encoding='latin1')
        logger.info(f'Pickled model loaded from {clf_path}')
        return clf
    except FileNotFoundError:
        logger.error(f'Pickled model `{clf_path}` was not found. Exiting.')
        sys.exit(2)
    except Exception as e:
        logger.warn('An unexpected error occurred while loading the model.')
        logger.error(e)
