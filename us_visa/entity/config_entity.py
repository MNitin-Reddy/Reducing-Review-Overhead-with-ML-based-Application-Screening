import os 
import sys 
from dotenv import load_dotenv
load_dotenv()

from us_visa.constants import *

from dataclasses import dataclass
from datetime import datetime


TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = os.getenv("PIPELINE_NAME")
    artifact_env_dir = os.getenv("ARTIFACT_DIR")
    artifact_dir: str = os.path.join(artifact_env_dir, TIMESTAMP)
    timestamp: str = TIMESTAMP


training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, os.getenv("DATA_INGESTION_DIR_NAME"))
    feature_store_file_path: str = os.path.join(data_ingestion_dir,  os.getenv("DATA_INGESTION_FEATURE_STORE_DIR"),  os.getenv("FILE_NAME"))
    training_file_path: str = os.path.join(data_ingestion_dir,  os.getenv("DATA_INGESTION_INGESTED_DIR"),  os.getenv("TRAIN_FILE_NAME"))
    testing_file_path: str = os.path.join(data_ingestion_dir,  os.getenv("DATA_INGESTION_INGESTED_DIR"), os.getenv("TEST_FILE_NAME"))
    train_test_split_ratio: float =  os.getenv("DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO")
    collection_name:str =  os.getenv("DATA_INGESTION_COLLECTION_NAME")

