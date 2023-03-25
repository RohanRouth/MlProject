import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    pre_processor_obj_file_path= os.path.join('Artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def get_data_transformer_object(self):
        "Function to handle Data transformation"

        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline = Pipeline(
                steps=[("Imputer",SimpleImputer(strategy="median")),
                       ("Scaler",StandardScaler())]
            
            )
            
            cat_pipeline = Pipeline(
                steps=[("Imputer",SimpleImputer(strategy="most_frequent")),
                       ("one_hot_encoder",OneHotEncoder()),
                       ("Scaler",StandardScaler(with_mean = False))
                       ]
            )

            logging.info("Numerical columns standard scaling Completed")
            logging.info("Categorical columns Encoding Completed")

            preprocessor = ColumnTransformer(
                [("num_pipeline",num_pipeline,numerical_columns),
                 ("cat_pipeline",cat_pipeline,categorical_columns)  
                 
            
                ]
            
            )

            return preprocessor



        except Exception as e:
            raise CustomException(e,sys)
            
    def Initiate_data_Transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading test and train data completed")
            logging.info("Obtaining PreProcessor Object")

            Pre_Processor = self.get_data_transformer_object()

            target_column="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_features_train_df = train_df.drop(columns=[target_column],axis=1)
            target_feature_train_df= train_df[target_column]

            input_features_test_df = test_df.drop(columns=[target_column],axis=1)
            target_features_test_df = test_df[target_column]

            logging.info(
                "Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=Pre_Processor.fit_transform(input_features_train_df)
            input_feature_test_arr=Pre_Processor.transform(input_features_test_df)

            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr,np.array(target_features_test_df)]

            logging.info("Saved preprocessing object")

            save_object(
                file_path = self.data_transformation_config.pre_processor_obj_file_path,
                obj=Pre_Processor

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.pre_processor_obj_file_path,
            )


        except Exception as e:
            raise CustomException(e,sys)
        
            