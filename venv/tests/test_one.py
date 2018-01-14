import pytest

# import the class want to test here
from Extractor.twitter import TwitterExtractor


@pytest.fixture()
def twitter(self):
    # set up for test
    return TwitterExtractor()


def test_one(self, twitter):
    x = "here"
    assert 'here' in x
