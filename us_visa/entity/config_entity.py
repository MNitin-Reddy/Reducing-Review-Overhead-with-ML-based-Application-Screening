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


@dataclass 
class DataValidationConfig:
    data_validation_dir = os.path.join(training_pipeline_config.artifact_dir,os.getenv("DATA_VALIDATION_DIR_NAME"))
    drift_report_file_path = os.path.join(data_validation_dir,os.getenv("DATA_VALIDATION_DRIFT_REPORT_DIR"), os.getenv("DATA_VALIDATION_DRIFT_REPORT_FILE_NAME"))


@dataclass
class DataTransformationConfig:
    data_transforamtion_dir = os.path.join(training_pipeline_config.artifact_dir, os.getenv("DATA_TRANSFOMATION_DIR_NAME"))
    transformed_train_file_path = os.path.join(data_transforamtion_dir, os.getenv("DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR"), (os.getenv("TRAIN_FILE_NAME")).replace("csv","npy"))
    transformed_test_file_path = os.path.join(data_transforamtion_dir, os.getenv("DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR"), (os.getenv("TEST_FILE_NAME")).replace("csv","npy"))
    transformed_object_file_path = os.path.join(data_transforamtion_dir, os.getenv("DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR"), os.getenv("PREPROCESSING_OBJECT_FILE_NAME"))

@dataclass
class ModelTrainerConfig:
    model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, os.getenv("MODEL_TRAINER_DIR"))
    trained_model_file_path: str = os.path.join(model_trainer_dir, os.getenv("MODEL_TRAINER_TRAINED_MODEL_DIR"), os.getenv("MODEL_FILE_NAME"))
    expected_accuracy: float = float(os.getenv("MODEL_TRAINER_EXPECTED_SCORE"))
    model_config_file_path: str = os.getenv("MODEL_TRAINER_MODEL_CONFIG_FILE_PATH")


@dataclass
class ModelEvaluationConfig:
    changed_threshold_score: float = float(os.getenv("MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE"))
    bucket_name: str = os.getenv("MODEL_BUCKET_NAME")
    s3_model_key_path: str = os.getenv("MODEL_FILE_NAME")

@dataclass
class ModelPusherConfig:
    bucket_name: str = os.getenv("MODEL_BUCKET_NAME")
    s3_model_key_path: str = os.getenv("MODEL_FILE_NAME")


@dataclass
class USvisaPredictorConfig:
    model_file_path: str = os.getenv("MODEL_FILE_NAME")
    model_bucket_name: str = os.getenv("MODEL_BUCKET_NAME")


