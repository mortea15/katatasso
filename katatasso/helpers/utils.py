#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import sys
import os

import tqdm

from katatasso.helpers.const import FN_MODEL
from katatasso.helpers.logger import rootLogger as logger

# Force the progress bar to be displayed regardless
# of verbosity settings. Useful for training on large data sets
FORCE_BAR = bool(int(os.getenv('FORCE_BAR', '0')))


def progress_bar(it):
    if logger.level < 30 or FORCE_BAR:
        return tqdm.tqdm(it)
    else:
        return it


def save_obj(obj, filepath):
    try:
        with open(filepath, 'wb') as f:
            pickle.dump(obj, f)
        logger.debug(f'Pickled object `{filepath}` saved to disk.')
    except Exception as e:
        logger.critical(f'An unexpected error occurred while saving the object `{filepath}`.')
        logger.error(e)


def load_obj(filepath):
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


def save_model(model, version='v2', algo='mnb'):
    fname = f'{FN_MODEL}{version}-{algo}.p'
    save_obj(model, fname)


def load_model(version='v2', algo='mnb'):
    fname = f'{FN_MODEL}{version}-{algo}.p'
    return load_obj(fname)


def save_vectorizer(vectorizer, algo='mnb'):
    fn = f'vectorizer_v2-{algo}.p'
    save_obj(vectorizer, fn)


def load_vectorizer(algo='mnb'):
    fn = f'vectorizer_v2-{algo}.p'
    return load_obj(fn)
