#!/usr/bin/env python3
import os
import sqlite3
import sys
import random
from collections import Counter

from katatasso.helpers.const import CLF_DICT_NUM, CLF_TRAININGDATA_PATH, DBFILE
from katatasso.helpers.logger import rootLogger as logger
from katatasso.helpers.utils import (load_vectorizer, progress_bar,
                                     save_vectorizer)

try:
    from sklearn.preprocessing import StandardScaler
    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
    import emailyzer
    import juicer
    import pandas as pd
except ModuleNotFoundError as e:
    logger.critical(f'Module `{e.name}` not found. Please install before proceeding.')
    sys.exit(2)


def warn_failed(failed):
    logger.critical(f'An error occurred with {len(failed)} files. See `failed.out` for filenames.')
    try:
        fail_cat = {
            'legit': len([fn for fn in failed if fn.startswith('legit')]),
            'spam': len([fn for fn in failed if fn.startswith('spam')]),
            'phish': len([fn for fn in failed if fn.startswith('phish')]),
            'malware': len([fn for fn in failed if fn.startswith('malware')]),
            'fraud': len([fn for fn in failed if fn.startswith('fraud')])
        }
        logger.critical(f'Failed:\n{fail_cat}')
    except:
        pass
    with open('failed.out', 'w') as f:
        f.write('\n'.join(failed))


def get_all_tags():
    try:
        conn = sqlite3.connect(DBFILE)
        c = conn.cursor()
        c.execute('SELECT filepath, tag, text, hosts FROM tags')
        res = c.fetchall()
        return res
    except Exception as e:
        logger.critical(f'Unable to fetch tags from database.')
        logger.error(e)
        sys.exit(2)


def get_n_tags(n):
    cats = [0, 1, 2, 3, 4]
    res = []
    try:
        conn = sqlite3.connect(DBFILE)
        c = conn.cursor()
        for cat in cats:
            try:
                c.execute('SELECT filepath, tag, text, hosts FROM tags WHERE tag=?', (cat,))
                tags = c.fetchall()
                if n <= len(tags):
                    res += random.sample(tags, n)
                else:
                    logger.warn(f'n={n} is higher than the number of samples in {cat}. Selecting {len(tags)} (all) samples.')
                    res += random.sample(tags, len(tags))
            except Exception as e:
                logger.critical(f'Unable to fetch {n} tags for category {cat}.')
                logger.error(e)
        return res
    except Exception as e:
        logger.critical(f'Unable to fetch tags from database.')
        logger.error(e)
        sys.exit(2)


# Get the file paths
def get_file_paths():
    logger.debug(f'Retrieving files from {CLF_TRAININGDATA_PATH}..')
    files = os.listdir(CLF_TRAININGDATA_PATH)
    logger.debug(f'     Found {len(files)} files in dir')
    file_paths = [CLF_TRAININGDATA_PATH + filename for filename in files if filename.endswith('.msg') or filename.endswith('.eml')]
    logger.debug(f'     Found {len(file_paths)} MSG/EML files in dir')
    logger.debug(f'         MSG: {len([filename for filename in file_paths if filename.endswith(".msg")])} || EML: {len([filename for filename in file_paths if filename.endswith(".eml")])}')
    return file_paths


# Create a data set for the classification
def make_dataset(dictionary):
    failed = []
    features = []
    labels = []
    tags = get_all_tags()
    if tags:
        logger.debug(f'Creating dataset from {len(tags)} entries')
        for filepath, tag, text, hosts in progress_bar(tags):
            try:
                data = []
                words = text.split()
                for entry in dictionary:
                    data.append(words.count(entry[0]))
                features.append(data)
                labels.append(tag)
            except AttributeError:
                failed.append(filepath.replace(CLF_TRAININGDATA_PATH, ''))
                pass
        if failed:
            warn_failed(failed)
        
    return features, labels


# Make a dictionary of the most frequent words
def make_dictionary():
    failed = []
    tags = get_all_tags()
    words = []
    logger.debug('Creating dictionary..')
    if tags:
        for filepath, tag, text, hosts in progress_bar(tags):
            try:
                words += text.split()
            except AttributeError:
                failed.append(filepath.replace(CLF_TRAININGDATA_PATH, ''))
                pass

        # Remove non-alphanumeric values
        words = [word for word in words if word.isalpha()]

        # Get the count of each word
        dictionary = Counter(words)

        if failed:
            warn_failed(failed)

        return dictionary.most_common(CLF_DICT_NUM)
    else:
        logger.error('No tags were found in the database.')
        return None


def create_dataframe(n=None):
    labels = []
    contents = []
    if n:
        tags = get_n_tags(n)
    else:
        tags = get_all_tags()
    if tags:
        for filepath, tag, text, hosts in progress_bar(tags):
            contents.append(text)
            labels.append(tag)

        return pd.DataFrame(list(zip(labels, contents)), columns = ['label', 'message'])
    else:
        logger.error('No tags were found in the database.')
        return None


def __create_dataframe():
    failed = []
    labels = []
    contents = []
    tags = get_all_tags()
    tagger = juicer.initStanfordNERTagger()
    if tags:
        for filepath, tag in progress_bar(tags):
            try:
                email = emailyzer.from_file(filepath)
                content = email.html_as_text
                # Preprocess, extract entities
                words = juicer.extract_stanford(content, named_only=False, stemming=False, tagger=tagger)
                contents.append(words)
                labels.append(tag)
            except AttributeError:
                failed.append(filepath.replace(CLF_TRAININGDATA_PATH, ''))
                pass
        df = pd.DataFrame(list(zip(labels, contents)), columns = ['label', 'message'])

        if failed:
            warn_failed(failed)

        return df
    else:
        logger.error('No tags were found in the database.')
        return None


def process_dataframe(df, algo='mnb'):
    df['message'] = df.message.map(lambda val: val.lower())
    df['message'] = df.message.str.replace('[^\w\s]', '')

    # Count occurrences
    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(df['message'])
    save_vectorizer(vectorizer, algo=algo)
    # Term Frequency Inverse Document Frequency
    transformer = TfidfTransformer().fit(counts)
    counts = transformer.transform(counts)

    return counts, df


def get_tfidf_counts(input, algo='mnb'):
    words = juicer.extract_stanford(input, named_only=False, stemming=False)
    text = words.lower()
    text = text.replace('[^\w\s]', '')

    vectorizer = load_vectorizer(algo=algo)
    counts = vectorizer.transform([text])

    # Term Frequency Inverse Document Frequency
    transformer = TfidfTransformer().fit(counts)
    counts = transformer.transform(counts)
    return counts


def standardize(x_train, x_test):
    scaler = StandardScaler(with_mean=False)
    scaler.fit(x_train)

    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)

    return x_train, x_test
