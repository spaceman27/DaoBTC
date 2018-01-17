""" Guide Line:
    User Twitter REST API against its rate limitation
    https://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively
"""
from pprint import pprint
from functools import reduce
from tweepy import OAuthHandler, AppAuthHandler
from tweepy import API
import re
import pymongo
from Extractor.absparser import AbsParser
from DataAccess.db import DBContext

""" Extract Data from Twitter from hundreds account
    Filter out positive status
    Cache old data and store unread status for review
"""

class TwitterExtractor(AbsParser):
    __api = None

    # Configuration
    __priorityCoin = ['ripple', 'vergecurrency', 'StellarLumens', 'CardanoStiftung'] # only search coin in a limited list
    __TimeLineMode = 0  # to request more tweets but only latest tweet
    __friendMode = 1  # 1: search all friend list, 0: search user in a predefined list
    __getRetweet = 1  # search retweet of status
    __appMode = None
    __ctx = DBContext()

    # May have to do rotation in a predefined username and access token list to get more request per 15'
    __username = "daongBTC"

    # Table name const in MongoDB
    __tweets = "tweets"
    __read_tweets = "read_tweets"
    __processing_tweets = "processing_tweets"
    __searchTerms = 'search_terms'

    def __init__(self, appMode=None, ckey=None, csecret=None, atoken=None, asecret=None):
        __appMode = appMode
        # consumer key, consumer secret, access token, access secret.
        # TODO: should move to database for configurable
        ckey = "uR8U5VlNwZiPdVx90hg2vpA8s" if ckey is None else ckey
        csecret = "xqPthljYXU18LSggR8kqtGlyUwjIcsfRknCXpXLGtVh6XKJI2M" if csecret is None else csecret
        atoken = "942670843783663616-6gLK5Uhdwnn8TxVTTVlMybfDUJCpOi5" if atoken is None else atoken
        asecret = "gw3Wez40PtSk8ykXMxUq4dzXiZSEdEeLVBJ4xFHTyShII" if asecret is None else asecret

        # App Mode Authentication or Access Token Mode
        if appMode:
            auth = AppAuthHandler(ckey, csecret)
        else:
            auth = OAuthHandler(ckey, csecret)
            auth.set_access_token(atoken, asecret)

        self.__api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        super()

    def process(self, filter_words, count=1):
        """Run Twitter Rest Api to extract data
        Args:
            filter_words: list of keyword want to search for
            count: limited result per friend user
        Returns:
            None
        """
        user = self.__api.get_user(self.__username)

        # print user.screen_name
        # print user.followers_count
        if self.__appMode == 1 and self.__TimeLineMode == 1:
            self.get_timeline(filter_words)
        else:
            if self.__friendMode:
                print("Getting all Twitter Friends \n")
                for friend in user.friends():
                    self.get_tweet(friend.screen_name, filter_words, count)
            else:
                for screen_name in self.__priorityCoin:
                    self.get_tweet(screen_name, filter_words, count)
        print('Twitter Data Extraction done!!')

    def get_timeline(self, filter_words, count=50000):
        data = self.__api.home_timeline(None, None, count)
        for status in data:
            if any(re.findall(reduce(lambda x, y: '%s|%s' % (x, y), filter_words), status.text)):
                self.process_status(status)
            if self.__getRetweet:
                self.get_retweet(status.id, filter_words)

    def get_tweet(self, username, filter_words, count=2):
        data = self.__api.user_timeline(username, count=count)
        # print status.user.screen_name
        tweets = []
        dup_dict = {}  # Filter out duplicated id
        for status in data:
            tweet = {
                "id": status.id,
                "created": status.created_at,
                "message": status.text
            }
            if status.id not in dup_dict:
                tweets.append(tweet)
            # if any(re.findall(reduce(lambda x, y: '%s|%s' % (x, y), filter_words), status.text)):
            #     self.process_status(status)
            # if self.__getRetweet:
            #     self.get_retweet(status.id, filter_words)

        # Store ALL Message to processing_tweet table

        try:
            self.__ctx.empty(self.__processing_tweets)
            self.__ctx.insert_many(self.__processing_tweets, tweets, 'message')
            print("Storing Status to DB done")
        except ServerSelectionTimeoutError as e:
            print("Failed to store status to DB !!")
            raise e

        # Fulltext search base on filter list
        for keyword in filter_words:
            result = self.__ctx.search(self.__processing_tweets, keyword)
            for message in result:
                pprint(message)
        print('total %s result', len(filter_words))

    def get_retweet(self, post_id, filter_words, count=1):
        data = self.__api.retweets(post_id, count)
        for status in data:
            if any(re.findall(reduce(lambda x, y: '%s|%s' % (x, y), filter_words), status.text)):
                self.process_status(status)

    def process_status(self, status):
        # process status here
        print("\n##id: %s [:] ##created at: %s \n ##content: %s", status.id, status.created_at, status.text)
