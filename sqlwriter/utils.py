# -*- coding: utf-8 -*-
'''
Created Friday August 1, 2017
Purpose: utility functions that Sebastian finds useful
@author: sestenssoro
'''
import datetime as dt
import logging
import logging.handlers
import os
import sys

import yaml

data_tests = [
    ('int', int),
    ('float', float),
    ('datetime', lambda x: dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')),
    ('datetime', lambda x: dt.datetime.strptime(x, '%Y/%m/%d %H:%M:%S')),
    ('date', lambda x: dt.datetime.strptime(x, '%Y-%m-%d')),
    ('date', lambda x: dt.datetime.strptime(x, '%Y/%m/%d')),
]


def detect_data_type(value):
    for typ, test in data_tests:
        try:
            test(value)
            return typ
        except:
            continue
    return 'string'


def chunks(l, n):
    """Generator that splits a list into equal peices of length n

    Parameters
    ----------
    l: Array-like
        Array to be split
    n: Integer
        Length of each sub array
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


class MyLogger(object):
    """Logging object

    Parameters
    ----------
    prog: String
        name of program that is being logged
    to_console: Boolean, default True
        log to console

    Returns
    -------
    logger : Python logging object
    """

    def __init__(self, prog=None, to_console=True):
        if prog is None:
            prog = os.path.basename(sys.argv[0])
            if prog.endswith('.py'):
                prog = prog[:-3]

        self.my_logger = logging.getLogger(prog)
        if os.path.exists('log'):
            LOG_DIR = 'log'
        else:
            wd = os.getcwd()
            while True:
                pardir = os.path.abspath(os.path.join(wd, os.pardir))
                if pardir == wd:
                    LOG_DIR = None
                    break
                if os.path.exists(os.path.join(pardir, 'log')):
                    LOG_DIR = os.path.join(pardir, 'log')
                    break
                wd = pardir

        if LOG_DIR:
            LOG_FILENAME = os.path.join(LOG_DIR, prog + '.log')
        else:
            LOG_FILENAME = prog + '.log'

        self.my_logger.setLevel(logging.DEBUG)
        self.log_filename = LOG_FILENAME
        self.handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=5 * 1024 * 1024, backupCount=15)
        self.formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.handler.setFormatter(self.formatter)
        self.handler.setLevel(logging.DEBUG)
        self.my_logger.addHandler(self.handler)

        if to_console:
            self.consolehandler = logging.StreamHandler()
            self.consolehandler.setLevel(logging.INFO)
            self.consoleformatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            self.consolehandler.setFormatter(self.consoleformatter)
            self.my_logger.addHandler(self.consolehandler)

    def getLogger(self):
        return self.my_logger

    def getConsoleHandler(self):
        return self.consolehandler

    def getHandler(self):
        return self.handler


def mylogger():
    return MyLogger().getLogger()
