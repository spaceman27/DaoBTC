"""
    The Brain is here
    MAIN control all workflows:
        Data ingestion and filtering  -> social network, media stream, forums
        REST API for balance checking,
        Monitoring the price -> Make Decision when to Buying/Selling and push notification to the app
        Make robot order base on volume of users
"""
from Factory.dataparser import ParserFactory
from Extractor.twitter import TwitterExtractor
from DataAccess.dbconfig import DbConfig


def main():
    """ Use Global App Authentication Mode - pass 1
        Access Token by default None
    """
    config = DbConfig()
    search_keywords = config.get_search_term()
    twitter = TwitterExtractor(1)  # init with AppAuth to gain more request per 15'
    ParserFactory(twitter).process(search_keywords, 5)  # limit 5 result per user
    ParserFactory(twitter)


if __name__ == "__main__":
    main()
