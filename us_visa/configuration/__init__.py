import os
from datetime import date 


MONGODB_URL_KEY = "MONGODB_URL"  # Set up as Environment variable
DATABASE_NAME = "US_VISA" 
COLLECTION_NAME = "visa_data"

PIPELINE_NAME: str = "usvisa"
ARTIFACT_DIR: str = "artifact"

MODEL_FILE_NAME = "model.pkl"