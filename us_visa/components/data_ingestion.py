import os 
import sys 

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact

from us_visa.exception import CustomException
from us_visa.logger import logging

from us_visa.data_access.usvisa_data import USvisaData


class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):

        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)

    
    def export_data_into_feature_store(self)-> DataFrame:

        try:
            logging.info(f"Exporting data from MongoDB")
            usvisa_data = USvisaData()
            dataframe = USvisaData(collection_name= self.data_ingestion_config.collection_name)

            logging.info(f"shape of dataframe: {dataframe.shape}")

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")

            dataframe.to_csv(feature_store_file_path, index=False,header=True)

            return dataframe


        except Exception as e:
            raise CustomException(e,sys)


    def split_data_as_train_test(self, dataframe: DataFrame)-> None:

        logging.info("Entered split-data_as_train_test method of Data_ingestion.py")

        try:
            train_set , test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Data split into train and test")
            
            dir_path = os.oath.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info("Exporting train and test data to file path")

            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logging.info("Exported train and test data to file path")

            logging.info('Exiting split_data_as_train_test function in data_ingestion.py')

        except Exception as e:
            raise CustomException(e,sys) 

    def initiate_data_ingestion(self)-> DataIngestionArtifact:

        try:
            dataframe = self.export_data_into_feature_store()
            logging.info("Got data from MongoDB")

            self.split_data_as_train_test(dataframe)
            logging.info("Performed train test split on data")

            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path, test_file_path=self.data_ingestion_config.testing_file_path)

            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact 

        except Exception as e:
            raise CustomException(e,sys)