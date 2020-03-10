#!/usr/bin/env python3
import os
from collections import Counter

from katatasso.helpers.const import CLF_DICT_NUM, CLF_TRAININGDATA_PATH
from katatasso.helpers.logger import rootLogger as logger
from katatasso.helpers.utils import progress_bar


# Get the file paths
def get_file_paths():
    logger.debug(f'Retrieving files from {CLF_TRAININGDATA_PATH}..')
    files = os.listdir(CLF_TRAININGDATA_PATH)
    logger.debug(f'     Found {len(files)} files in dir')
    file_paths = [CLF_TRAININGDATA_PATH + filename for filename in files if filename.endswith('.msg') or filename.endswith('.eml')]
    logger.debug(f'     Found {len(file_paths)} MSG/EML files in dir')
    logger.debug(f'         MSG: {len([filename for filename in file_paths if filename.endswith(".msg")])} || EML: {len([filename for filename in file_paths if filename.endswith(".eml")])}')
    return file_paths


# Make a dictionary of the most frequent words
def make_dictionary():
    file_paths = get_file_paths()
    words = []
    logger.info('Creating dictionary..')
    for fp in progress_bar(file_paths):
        with open(fp, encoding='latin-1') as f:
            content = f.read()
            words += content.split()

    # Remove non-alphanumeric values
    words = [word for word in words if word.isalpha()]

    # Get the count of each word
    dictionary = Counter(words)

    return dictionary.most_common(CLF_DICT_NUM)
