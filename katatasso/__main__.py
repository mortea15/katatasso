#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import os
import sys

import katatasso
from katatasso.helpers.logger import increase_log_level
from katatasso.helpers.logger import rootLogger as logger
from katatasso.helpers.utils import prepare_result

current = os.path.realpath(os.path.dirname(__file__))
APPNAME = 'katatasso'


INDENT = '  '
HELPMSG = f'''usage: {APPNAME} [-h] (-f INPUT_FILE | -s) [-t] [-c] [-d FORMAT] [-o OUTPUT_FILE] [-v]

    {INDENT * 1}-f, --infile        {INDENT * 2}Extract entities from file
    {INDENT * 1}-s, --stdin         {INDENT * 2}Extract entities from STDIN

    {INDENT * 1}-t, --train         {INDENT * 2}Train and create a model for classification
    {INDENT * 1}-c, --classify      {INDENT * 2}Classify the text

    {INDENT * 1}-o, --outfile       {INDENT * 2}Output results to this file
    {INDENT * 1}-d, --format        {INDENT * 2}Output results as this format.
                              Available formats: [plain (default), json]

    {INDENT * 1}-v, --verbose       {INDENT * 2}Increase verbosity (can be used twice, e.g. -vv)
    {INDENT * 1}-h, --help          {INDENT * 2}Print this message
'''


def main():
    TEXT = None
    CONFIG = {}

    result = None

    if len(sys.argv) < 2:
        print(HELPMSG)
        logger.error('No input specified')
        sys.exit(2)
    
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, 'hf:stco:d:v', ['help', 'infile=', 'stdin', 'train', 'classify', 'outfile=', 'format=', 'verbose'])
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
    if opts_v > 2:
        opts_v = 2
    v = 0
    while v < opts_v:
        increase_log_level()
        v += 1
    
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
                logger.error(f'The specified file {file_path} does not exist.')
                sys.exit(2)
            except Exception as e:
                logger.error(f'An error occurred while reading the file `{file_path}`.')
                logger.error(e)
                sys.exit(2)
        elif opt in ('-s', '--stdin'):
            try:
                logger.debug(f'Using input from STDIN')
                TEXT = sys.stdin.read()
            except Exception as e:
                logger.error(e)
                sys.exit(2)
        elif opt in ('-t', '--train'):
                katatasso.train()
                logger.debug(f'ACTION: Creating model from dataset')
        elif opt in ('-c', '--classify'):
            if TEXT:
                logger.debug(f'ACTION: Classifying input')
                result = katatasso.classify(TEXT)
            else:
                logger.error(f'Missing input (specify using -f or -s)')
                sys.exit(2)
        elif opt in ('-o', '--outfile'):
            logger.debug(f'CONFIG: Setting output file to {arg}')
            CONFIG['outfile'] = arg
        elif opt in ('-d', '--format'):
            if arg in ['plain', 'json']:
                logger.debug(f'CONFIG: Setting output file format to {arg}')
                CONFIG['format'] = arg
            else:
                logger.error('Invalid format. Must be one of [plain, json]')
                sys.exit(2)
        
    if result:
        output = prepare_result(result)

        outfile = CONFIG.get('outfile')
        outformat = CONFIG.get('format')
        if outfile:
            ext = 'json' if outformat == 'json' else 'txt'
            fname = f'{outfile}.{ext}'
            if outformat == 'plain':
                with open(fname, 'w') as f:
                    f.write('\n'.join(output))
            elif outformat == 'json':
                import json
                with open(fname, 'w', encoding='utf-8') as f:
                    json.dump(output, f, ensure_ascii=False, indent=4)
            logger.info(f'Results saved to file `{fname}`')
            sys.exit(0)
        else:
            print(output)
            sys.exit(0)


if __name__ == '__main__':
    main()
