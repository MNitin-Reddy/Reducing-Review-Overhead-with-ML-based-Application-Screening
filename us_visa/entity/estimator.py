import sys

from pandas import DataFrame
from sklearn.pipeline import Pipeline

from us_visa.exception import CustomException
from us_visa.logger import logging

import optuna
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score



class TargetValueMapping:
    def __init__(self):
        self.Certified:int = 0
        self.Denied:int = 1
    def _asdict(self):
        return self.__dict__
    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(),mapping_response.keys()))
    

# class OptunaHyperparamTuner:
#     def __init__(self, X_train, y_train, X_test, y_test):
#         # Store datasets as class attributes
#         self.X_train = X_train
#         self.y_train = y_train
#         self.X_test = X_test
#         self.y_test = y_test

#     @staticmethod
#     def objective(trial, X_train, y_train, X_test, y_test):
#         # Generate hyperparameters using Optuna's suggest methods
#         model = trial.suggest_categorical('classifier', ['RandomForest', 'KNN'])

#         if model == 'RandomForest':
#             n_estimators = trial.suggest_int('n_estimators', 10, 20)
#             max_depth = trial.suggest_int('max_depth', 10, 200)
#             max_features = trial.suggest_categorical('max_features', ['sqrt', 'log2', None])
#             classifier_obj = RandomForestClassifier(n_estimators=n_estimators, 
#                                                     max_depth=max_depth, 
#                                                     max_features=max_features)

#         else: #model == 'KNN':
#             algorithm = trial.suggest_categorical('algorithm', ['auto', 'ball_tree', 'kd_tree', 'brute'])
#             n_neighbors = trial.suggest_int('n_neighbors', 3, 10)
#             weights = trial.suggest_categorical('weights', ['uniform', 'distance'])
#             classifier_obj = KNeighborsClassifier(algorithm=algorithm, 
#                                                   n_neighbors=n_neighbors, 
#                                                   weights=weights)

#         # else:  # XGBClassifier
#         #     max_depth = trial.suggest_int('max_depth', 3, 10)
#         #     min_child_weight = trial.suggest_int('min_child_weight', 1, 6)
#         #     classifier_obj = XGBClassifier(max_depth=max_depth, 
#         #                                    min_child_weight=min_child_weight)

#         # Fit the model on the training data
#         classifier_obj.fit(X_train, y_train)
        
#         # Predict on the test data
#         y_pred = classifier_obj.predict(X_test)

#         # Calculate accuracy
#         accuracy = accuracy_score(y_test, y_pred)

#         return accuracy  # Return accuracy as the objective value

#     def optimize(self, n_trials=50):
#         # Define the study with a direction to maximize accuracy
#         study = optuna.create_study(direction='maximize', sampler=optuna.samplers.TPESampler())
        
#         # Optimize the objective function using the datasets stored in the class
#         study.optimize(lambda trial: self.objective(trial, 
#                                                     self.X_train, self.y_train, 
#                                                     self.X_test, self.y_test), 
#                        n_trials=n_trials)

#         # Return the best trial's value and parameters
#         return study.best_trial.value, study.best_trial.params


class USvisaModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        """
        :param preprocessing_object: Input Object of preprocesser
        :param trained_model_object: Input Object of trained model 
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: DataFrame) -> DataFrame:
        """
        Function accepts raw inputs and then transformed raw input using preprocessing_object
        which guarantees that the inputs are in the same format as the training data
        At last it performs prediction on transformed features
        """
        logging.info("Entered predict method of UTruckModel class")

        try:
            logging.info("Using the trained model to get predictions")

            transformed_feature = self.preprocessing_object.transform(dataframe)

            logging.info("Used the trained model to get predictions")
            return self.trained_model_object.predict(transformed_feature)

        except Exception as e:
            raise CustomException(e, sys) from e

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"

    