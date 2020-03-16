#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from katatasso.helpers.logger import rootLogger as logger
from katatasso.modules.classifier import classify, classifyv2
from katatasso.modules.trainer import train, trainv2

try:
    import sklearn
except ModuleNotFoundError as e:
    logger.critical(f'Module `{e.name}` not found. Please install before proceeding.')
    sys.exit(2)
