import doctest
import pytest
from Extractor.twitter import TwitterExtractor


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(TwitterExtractor))
    return tests