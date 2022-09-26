from pymongo import MongoClient

import pymongo
import sys
from pymongo.errors import ServerSelectionTimeoutError

from app.constants.mongodb_constants import MongoCollections
from app.models.book import Book
from app.utils.logger_utils import get_logger
from config import MongoDBConfig

logger = get_logger('MongoDB')


class MongoDB:
    def __init__(self, connection_url=None):
        if connection_url is None:
            # connection_url = f'mongodb://{MongoDBConfig.USERNAME}:{MongoDBConfig.PASSWORD}@{MongoDBConfig.HOST}:{
            # MongoDBConfig.PORT}
            connection_url = f'mongodb://admin:admin123@localhost:27017/?authMechanism=DEFAULT&authSource=trainingBE'
        # self.connection_url = connection_url.split('@')[-1]
        try:
            self.client = pymongo.MongoClient(connection_url)
            logger.info(f"Connected to MongoDB server on {connection_url}")
        except ServerSelectionTimeoutError as e:
            logger.error(e)
            sys.exit(1)

        self.db = self.client[MongoDBConfig.DATABASE]
        self._books_col = self.db[MongoCollections.books]

    def get_books(self, filter_=None, projection=None):
        try:
            if not filter_:
                filter_ = {}
            cursor = self._books_col.find(filter_, projection=projection)
            # query = {"_id": "a368b6ae-fb7c-48e7-a252-f1bd59decd1c"}
            # book_obj = self._books_col.get_book(query)
            # print(Book().from_dict(book_obj))
            data = []
            for doc in cursor:
                data.append(Book().from_dict(doc))
            return data
        except Exception as ex:
            logger.exception(ex)
        return []

    def add_book(self, book: Book):
        try:
            inserted_doc = self._books_col.insert_one(book.to_dict())
            return inserted_doc
        except Exception as ex:
            logger.exception(ex)
        return None

    # TODO: write functions CRUD with books
    def get_book(self, filter_):
        try:
            got_doc = self._books_col.find_one(filter_)
            return got_doc
        except Exception as ex:
            logger.exception(ex)
        return []

    def update_book(self, filter_, update_operation):
        try:
            updated_doc = self._books_col.update_one(filter_, update_operation)
            return updated_doc
        except Exception as ex:
            logger.exception(ex)
        return []

    def delete_book(self, filter_):
        try:
            deleted_doc = self._books_col.delete_one(filter_)
            return deleted_doc
        except Exception as ex:
            logger.exception(ex)
        return None
