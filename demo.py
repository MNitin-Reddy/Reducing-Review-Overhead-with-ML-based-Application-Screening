from us_visa.pipeline.training_pipeline import TrainingPipeline
import os
from dotenv import load_dotenv
load_dotenv()

print(os.getenv("ARTIFACT_DIR"))
print(os.getenv("MONGODB_URL"))

obj = TrainingPipeline()
obj.run_pipeline()