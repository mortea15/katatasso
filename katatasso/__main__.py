#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import os
import sys

import katatasso
from katatasso.helpers.logger import increase_log_level, log_to_file
from katatasso.helpers.logger import rootLogger as logger
from katatasso.helpers.const import CATEGORIES

current = os.path.realpath(os.path.dirname(__file__))
APPNAME = 'katatasso'


INDENT = '  '
HELPMSG = f'''usage: {APPNAME} (-f INPUT_FILE | -s) [-t (v1 | v2)] [-c] [-d FORMAT] [-o OUTPUT_FILE] [-v] [-l]

    {INDENT * 1}-f, --infile        {INDENT * 2}Extract entities from file
    {INDENT * 1}-s, --stdin         {INDENT * 2}Extract entities from STDIN

    {INDENT * 1}-t, --train         {INDENT * 2}Train and create a model for classification. Specify either `v1` or `v2` as arg.
    {INDENT * 1}-c, --classify      {INDENT * 2}Classify the text. Specify either `v1` or `v2` as arg,
                              depending on what mode was used for training.

    {INDENT * 1}-o, --outfile       {INDENT * 2}Output results to this file
    {INDENT * 1}-d, --format        {INDENT * 2}Output results as this format.
                              Available formats: [plain (default), json]

    {INDENT * 1}-v, --verbose       {INDENT * 2}Increase verbosity (can be used several times, e.g. -vvv)
    {INDENT * 1}-l, --log-file      {INDENT * 2}Write log events to the file `{APPNAME}.log`
    {INDENT * 1}--help              {INDENT * 2}Print this message
'''


def main():
    TEXT = None
    CONFIG = {}

    result = {}

    if len(sys.argv) < 2:
        print(HELPMSG)
        logger.critical('No input specified')
        sys.exit(2)
    
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, 'hf:st:c:o:d:v', ['help', 'infile=', 'stdin', 'train=', 'classify=', 'outfile=', 'format=', 'verbose'])
    except getopt.GetoptError:
        print(HELPMSG)
        sys.exit(2)

    if not opts:
        print(HELPMSG)
        sys.exit(0)

    """
    Increase verbosity
    """
    opts_v = len(list(filter(lambda opt: opt == ('-v', ''), opts)))
    if opts_v > 4:
        opts_v = 4
    v = 0
    while v < opts_v:
        increase_log_level()
        v += 1
    
    """
    Log to file
    """
    if v > 0:
        enable_logfile = list(filter(lambda opt: opt[0] in ('-l', '--log-file'), opts))
        if enable_logfile:
            log_to_file()
    
    for opt, arg in opts:
        if opt == '--help':
            print(HELPMSG)
            sys.exit(0)
        elif opt in ('-f', '--infile'):
            file_path = arg
            logger.debug(f'Using input file {file_path}')
            try:
                with open(file_path, 'r') as f:
                    TEXT = f.read()
            except FileNotFoundError:
                logger.critical(f'The specified file {file_path} does not exist.')
                sys.exit(2)
            except Exception as e:
                logger.critical(f'An error occurred while reading the file `{file_path}`.')
                logger.error(e)
                sys.exit(2)
        elif opt in ('-s', '--stdin'):
            try:
                logger.debug(f'Using input from STDIN')
                TEXT = sys.stdin.read()
            except Exception as e:
                logger.critical(f'An error occurred while reading from stdin.')
                logger.error(e)
                sys.exit(2)
        elif opt in ('-t', '--train'):
            logger.debug(f'ACTION: Creating model from dataset')
            if arg == 'v1':
                katatasso.train()
            elif arg == 'v2':
                katatasso.trainv2()
            else:
                logger.critical(f'Please specify either `v1` or `v2`. E.g. `katatasso -t v2`')
                sys.exit(2)
        elif opt in ('-c', '--classify'):
            if TEXT:
                logger.debug(f'ACTION: Classifying input')
                if arg == 'v1':
                    category, accuracy = katatasso.classify(TEXT)
                elif arg == 'v2':
                    category, accuracy = katatasso.classifyv2(TEXT)
                else:
                    logger.critical(f'Please specify either `v1` or `v2`. E.g. `katatasso -c v2`')
                    sys.exit(2)
                result = { 'category': category, 'accuracy': accuracy, 'alias': CATEGORIES.get(category) }
            else:
                logger.critical(f'Missing input (specify using -f or -s)')
                sys.exit(2)
        elif opt in ('-o', '--outfile'):
            logger.debug(f'CONFIG: Setting output file to {arg}')
            CONFIG['outfile'] = arg
        elif opt in ('-d', '--format'):
            if arg in ['plain', 'json']:
                logger.debug(f'CONFIG: Setting output file format to {arg}')
                CONFIG['format'] = arg
            else:
                logger.critical('Invalid format. Must be one of [plain, json]')
                sys.exit(2)
        
    if result:
        outformat = CONFIG.get('format')
        outfile = CONFIG.get('outfile')
        if outfile:
            ext = 'json' if outformat == 'json' else 'txt'
            fname = f'{outfile}.{ext}'
            if outformat == 'plain':
                result['accuracy'] = int(result.get('accuracy'))
                with open(fname, 'w') as f:
                    f.write('\n'.join(list(result.values())))
            elif outformat == 'json':
                import json
                with open(fname, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=4)
            logger.debug(f'Results saved to file `{fname}`')
            sys.exit(0)
        else:
            print(result)
            sys.exit(0)


if __name__ == '__main__':
    main()
