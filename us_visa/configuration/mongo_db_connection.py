import os
import sys 

from us_visa.exception import CustomException
from us_visa.logger import logging 

from us_visa.constants import DATABASE_NAME, COLLECTION_NAME

import pymongo 
import certifi 

ca = certifi.where()

class MongoDBClient:
    """_summary_

    Raises:
        Exception: _description_
        CustomException: _description_
    """

    client = None

    def __init__(self, database_name = DATABASE_NAME) -> none:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL)
                if mongo_db_url is None:
                    raise Exception(f"Enironment key {MONGODB_URL} is not set.")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile = ca)
                self.client = MongoDBClient.client
                self.database = self.client[database_name]
                self.database_name = database_name
                logging.info("MongoDB connection succesful")
        except Exception as e:
            raise CustomException(e,sys)