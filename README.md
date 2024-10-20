
# Predicting US Visa Approvals with ML

![Python](https://img.shields.io/badge/Python-3.8-FFD43B?style=for-the-badge&logo=python&logoColor=blue) ![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white) ![sklearn](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

![GitHubActions](https://img.shields.io/badge/CI_CD_-_GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20ECR%20%7C%20S3Bucket-FFDE21?style=for-the-badge&logoColor=yellow)  ![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

![MLflow](https://img.shields.io/badge/MLflow-experiment%20tracking-0041C2?style=for-the-badge&logoColor=green.svg) ![Optuna](https://img.shields.io/badge/Optuna-hyperparameter--tuning-2B547E?style=for-the-badge&logoColor=orange.svg) ![Evidently](https://img.shields.io/badge/Evidently-data%20validation-DB0F27?style=for-the-badge&logoColor=brightgreen)  






  The Immigration and Nationality Act (INA) of the United States permits foreign workers to work temporarily or permanently. It also protects US workers from adverse impacts in the workplace and enforces strict hiring requirements when employers seek to fill workforce shortages with foreign employees. These immigration programs are managed by the Office of Foreign Labor Certification (OFLC).

## Problem Statement
The OFLC processes job certification applications from organizations looking to bring foreign workers to the United States. With an increasing volume of applications, a machine learning model is needed to efficiently shortlist visa applicants.

* This project creates a classification model that determines whether a visa application should be approved or denied. The model not only forecasts results, but it also recommends profiles that are more likely to be accepted, so streamlining the decision-making process.


## Data Collection
The dataset used in this project is provided by the Office of Foreign Labor Certification (OFLC).

## Tech Stack
* **Python:** Core programming language
* **MongoDB:** Data storage
* **Evidently:** Data validation and monitoring
* **Optuna:** Hyperparameter tuning
* **MLflow:** Experiment tracking
* **GitHub Actions:** CI/CD pipeline
* **Docker:** Containerization
* **AWS (EC2, ECR):** Deployment platform


## Exploratory Data Analysis:
### Initial Analysis Report
* __no_of_employees__ has many outliers which can be Handled in Feature Engineering and no_of_employees is Right Skewed.
* __yr_of_estab__ is left skewed and some outliers below the lower bound of Box plot.
* __prevailing_wage__ is right skewed with outliers above upper bound of box plot.
* There are No missing values in the dataset.
* The __case_id__ column can be deleted because each row has unique values.
* The case_status column is the target to predict.
* In the Categorical column, features can be made Binary/ numerical in feature Encoding

### Final Analysis
* __case_id__ column can be dropped as it is an ID.
* __requires_job_training__ column can be dropped as it doesn't have much impact on target variable, Proved in visualization and __chi2 test__.
* __no_of_employees__, __prevailing_wage__ columns have outllier which should be handled.
* __continent__ columns has few unique values with very less count, which can be made as others.
* Target column __case_status__ is imbalanced should be handled with techniques like __SMOTE__ before model building.

## Flow of project

* **Data Ingestion:** Load and store raw data from MongoDB to artifacts.
* **Data Validation:** Validate schema and detect data drift using Evidently.
* **Feature Engineering:** Handle missing values, encode categorical variables, and scale numerical features.
* **Feature Selection:** Apply multicollinearity analysis and chi-squared tests to select key features.
* **Model Training:** Train on various calssification models and fins the best base model.
* **Hyperparameter Tuning:** Use Optuna to optimize model parameters.
* **Experiment Tracking:** Log results and experiments with MLflow.
* **CI/CD:** Automate evaluation and deployment using GitHub Actions.
* **Deployment:** Use Docker to deploy the application on AWS EC2 via ECR.

## Pipeline Workflow

![USVisa flowchart](https://github.com/user-attachments/assets/8b61c924-490a-4c7c-b763-5e785beee63b)

## Installation

Clone repository:
```bash
git clone https://github.com/MNitin-Reddy/US-Visa-Approval-Prediction.git

```
Create a python virtual environment and install dependencies:
```bash
conda create -n venv python=3.8
conda activate venv
pip install -r requirements.txt
```
Run pipeline: (Ensure if MLflow server is running to track experiments)
```bash
python demo.py
```
Run web app:
```bash
python app.py
```
Checking experiments using MLflow:
```bash
mlflow ui 
```


## CI/CD using GitHub Actions and Deployment with AWS

### 1. Login to AWS console.

### 2. Create IAM user for deployment

	#with specific access to 

	1. Amazon EC2: AmazonEC2FullAccess

	2. Amazon ECR: AmazonEC2ContainerRegistryFullAccess

    (Copy the Access key and Secret Access Key for the user)

### 3. Create ECR repo to store/save docker image
    - Save the URI: (315865595366.dkr.ecr.us-east-1.amazonaws.com/visarepo) [This is a sample uri]

### 4. Create EC2 machine (Ubuntu) 

### 5. Open EC2 and Install docker in EC2 Machine:
	
	
	#optinal

	sudo apt-get update -y

	sudo apt-get upgrade
	
	#required

	curl -fsSL https://get.docker.com -o get-docker.sh

	sudo sh get-docker.sh

	sudo usermod -aG docker ubuntu

	newgrp docker

##### Description: About the deployment

	1. Build docker image of the source code

	2. Push docker image to ECR

	3. Launch Your EC2 

	4. Pull Your image from ECR in EC2

	5. Lauch your docker image in EC2
	
### 6. GitHub Actions
    1. Configuring EC2 as self-hosted runner
        In your github repo:
            setting > actions > runner > new self hosted runner> choose os > then run command one by one

    2. Create a folder on repo .github ->  workflows -> aws.yaml -> copy the CI/CD template for aws deployment



### 7. Github secrets or environment variables to setup:

   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_DEFAULT_REGION
   - ECR_REPO_URI
   - MONGODB_URI

Now everytime we commit to the repo Github Actions automatically deploys the new code to the AWS cloud.


## Conclusion

With an accuracy of 93%, the best-performing model in this project is K-Nearest Neighbors (KNN). After hyperparameter tuning using Optuna and handling target column imbalance using SMOTE, the optimal parameters were:

* algorithm: "brute"
* weights: "distance"
* no_of_neighbors: 5
This model effectively predicted visa approvals by leveraging the most relevant features identified through multicollinearity checks and chi-squared tests.

MLflow ensured comprehensive tracking of experiments, while the integration of CI/CD pipelines with GitHub Actions automated testing and deployment.
The final solution is containerized using Docker and deployed seamlessly on AWS. MongoDB supports persistent data storage, ensuring reliability across deployments.


