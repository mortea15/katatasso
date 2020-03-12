#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from katatasso.helpers.logger import rootLogger as logger
from katatasso.modules.classifier import classify
from katatasso.modules.trainer import train, trainv2

try:
    import sklearn
except ModuleNotFoundError:
    logger.error(f'Module scikit-learn not found. Please install before proceeding.')
    sys.exit(2)
