""" Guide Line:
"""
from pprint import pprint
from functools import reduce
import re
import pymongo
from Extractor.absparser import AbsParser
from DataAccess.db import DBContext


class FacebookExtractor(AbsParser):
    """ Extract Data from Facebook from hundreds account
        Filter out positive status
        Cache old data and store unread status for review
    """
    __api = None

    # Configuration
    __ctx = DBContext()

    # May have to do rotation in a predefined username and access token list to get more request per 15'
    __username = "daongBTC"

    # Table name const in MongoDB

    def __init__(self):
        super()

    def process(self, filter_words, count=1):
        pass
