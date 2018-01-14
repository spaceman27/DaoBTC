from pprint import pprint
from pymongo import MongoClient
import datetime


class DBContext:
    __db = None
    __tweets = None
    __processing = None
    __read_tweets = None

    def __init__(self):
        mongo = MongoClient('mongodb://localhost:27017')
        self.__db = mongo.crypto
        self.__tweets = self.__db.tweets
        self.__processing = self.__db.processing_tweets

    def find_all(self, collection):
        """Fetch all records in on table
        Args:
            Table name in string
        Returns:
            An iterable
        """
        collection = self.__db[collection]
        return collection.find({})

    def get_collection(self, name):
        """Get mongo collection
        Args:
            Table name in string
        Returns:
            Mongo collection object
        """
        return self.__db[name]

    def empty(self, collection):
        """Remove all records in a mongo collection
        Args:
            Table name in string
        Returns:
            None
        """
        collection = self.__db[collection]
        collection.remove()

    def insert_many(self, collection, tweets, options=None):
        """Insert a collection to mongo db
        Args:
            collection: table name in string
            tweets: a list of tweets
            options: format should be { "field want to create index", ... }
        Returns:
            None
        """

        collection = self.__db[collection]
        collection.insert_many(tweets)
        if options is not None:
            collection.create_index(options)

    def insert_one(self, collection, tweet):
        """Insert a record to mongo db
        Args:
            collection: table name in string
            tweet: a single tweet object
        Returns:
            None
        """
        collection = self.__db[collection]
        collection.insert_one(tweet)

    def search(self, collection, keyword):
        """Fulltext search mongo build-in function
        Args:
            collection: table name in string
            keyword: keyword want to search
        Returns:
            a iterable of all result orderd by score rank
        """
        collection = self.__db[collection]
        return collection.find({"$text": {"$search": keyword}})
