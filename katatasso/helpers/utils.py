#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import sys

import tqdm

from katatasso.helpers.const import FP_MODEL
from katatasso.helpers.logger import rootLogger as logger


def progress_bar(it):
    if logger.level < 30:
        return tqdm.tqdm(it)
    else:
        return it


def __save_obj(obj, filepath):
    try:
        with open(filepath, 'wb') as f:
            pickle.dump(obj, f)
        logger.debug(f'Pickled object `{filepath}` saved to disk.')
    except Exception as e:
        logger.critical(f'An unexpected error occurred while saving the object `{filepath}`.')
        logger.error(e)


def __load_obj(filepath):
    try:
        with open(filepath, 'rb') as f:
            obj = pickle.load(f, encoding='latin1')
        logger.debug(f'Pickled object loaded from `{filepath}`.')
        return obj
    except FileNotFoundError:
        logger.critical(f'Pickled object `{filepath}` was not found. Exiting.')
        sys.exit(2)
    except Exception as e:
        logger.critical(f'An unexpected error occurred while loading the object `{filepath}`.')
        logger.error(e)
        sys.exit(2)


def save_model(model):
    __save_obj(model, FP_MODEL)


def load_model():
    return __load_obj(FP_MODEL)


def save_y_test(y_test):
    __save_obj(y_test, f'y_test-{FP_MODEL}')


def load_y_test():
    return __load_obj(f'y_test-{FP_MODEL}')


def save_vectorizer(vectorizer):
    __save_obj(vectorizer, f'vectorizer-{FP_MODEL}')


def load_vectorizer():
    return __load_obj(f'vectorizer-{FP_MODEL}')
