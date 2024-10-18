import sys 
import json 
import os
from dotenv import load_dotenv
load_dotenv()

from datetime import date

import pandas as pd 
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection

from us_visa.entity.config_entity import DataValidationConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact

from us_visa.logger import logging
from us_visa.exception import CustomException
from us_visa.utils.main_utils import read_yaml_file, write_yaml_file


class DataValidation:

    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config =  read_yaml_file(file_path=os.getenv("SCHEMA_FILE_PATH_URL"))
        except Exception as e:
            raise CustomException(e,sys)


    def validate_number_of_columns(self, dataframe:pd.DataFrame)-> bool:
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Are required columns present: {status}")
            return status

        except Exception as e:
            raise CustomException(e,sys)

    def is_column_exist(self, df:pd.DataFrame)-> bool:
        try:
            df_columns = df.columns
            missing_numerical_cols = []
            missing_categorical_cols = []
            for col in self._schema_config["numerical_columns"]:
                if col not in df_columns:
                    missing_numerical_cols.append(col)

            if len(missing_numerical_cols)>0:
                logging.info(f"Missing numerical columns: {missing_numerical_cols}")
            
            for col in self._schema_config["categorical_columns"]:
                if col not in df_columns:
                    missing_categorical_cols.append(col)

            if len(missing_categorical_cols)>0:
                logging.info(f"Missing categorical columns: {missing_categorical_cols}")

            return False if len(missing_numerical_cols)>0 or len(missing_categorical_cols) > 0 else True

        except Exception as e:
            raise CustomException(e,sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)

    def detect_data_drift(self, reference_df: pd.DataFrame, current_df: pd.DataFrame)-> bool:
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])

            data_drift_profile.calculate(reference_df, current_df)

            report = data_drift_profile.json()

            json_report = json.loads(report)

            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content= json_report)

            n_features = json_report['data_drift']['data']["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]

            logging.info(f"{n_drifted_features}/{n_features} drift detected.")
            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]
            return drift_status

        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_validation(self)-> DataValidationArtifact:

        try:
            validation_error_msg = ""
            logging.info("Starting data validation")
            train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                                 DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))

            status = self.validate_number_of_columns(dataframe=train_df)
            logging.info(f"All required columns present in training dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."


            status = self.validate_number_of_columns(dataframe=test_df)
            logging.info(f"All required columns present in testing dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in test dataframe."


            status = self.is_column_exist(df=train_df)
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."

            status = self.is_column_exist(df=test_df)
            if not status:
                validation_error_msg += f"columns are missing in test dataframe."

            validation_status = len(validation_error_msg) == 0

            if validation_status:
                drift_status = self.detect_data_drift(train_df, test_df)
                if drift_status:
                    logging.info(f"Drift detected.")
                    validation_error_msg = "Drift detected"
                else:
                    validation_error_msg = "Drift not detected"
            else:
                logging.info(f"Validation_error: {validation_error_msg}")
                

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact
            
        except Exception as e:
            raise CustomException(e,sys)


        