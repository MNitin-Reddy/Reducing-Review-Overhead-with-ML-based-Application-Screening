import sys 

from us_visa.exception import CustomException
from us_visa.logger import logging

from us_visa.components.data_ingestion import DataIngestion
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from us_visa.entity.config_entity import DataIngestionConfig, DataValidationConfig

from us_visa.components.data_validation import DataValidation

class TrainingPipeline:

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()


    def start_data_ingestion(self)-> DataIngestionArtifact:
        try:

            logging.info("entered start-data_ingestion in trainiing_pipeline.py")
            logging.info("Getting data from MongoDB")

            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Got train and test dataset")
            logging.info("Exited start_data_ingestion of training pipeline")

            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)


    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact)-> DataValidationArtifact:
        try:
            logging.info("Entered the start_data_validation method of TrainPipeline class")

            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")
            logging.info("Exited the start_data_validation method of TrainPipeline class")

            return data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)


    def run_pipeline(self) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise CustomException(e,sys)
