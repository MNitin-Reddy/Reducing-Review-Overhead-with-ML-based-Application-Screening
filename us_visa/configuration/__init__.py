import os
from datetime import date 


MONGODB_URL_KEY = "MONGODB_URL"  # Set up as Environment variable
DATABASE_NAME = "US_VISA" 
COLLECTION_NAME = "visa_data"

PIPELINE_NAME: str = "usvisa"
ARTIFACT_DIR: str = "artifact"

FILE_NAME = "usvisa.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

MODEL_FILE_NAME = "model.pkl"


"""
 Data Ingestion constants
"""

DATA_INGESTION_COLLECTION_NAME = 'visa_data'
DATA_INGESTION_DIR_NAME = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2



