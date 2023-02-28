from Insurance_Project.entity import artifact_entity,config_entity
from Insurance_Project.exception import InsuraneceException
import os,sys
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
import pandas as pd
import numpy as np
from Insurance_Project.config import TARGET_COLUMN
from sklearn.preprocessing import LabelEncoder

## Missing values impute
## Outliers handling
## imbalanced handling
## convert categorical data into numerical data

class DataTransformation:
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,data_ingestion_artifact:artifact_entity.DataIngestionArtifact):

        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise InsuraneceException(e,sys)


    @classmethod
    def get_data_transformer_object(cls)->Pipeline:

        try:
            simple_imputer = SimpleImputer(strategy = 'constant',fil_values = 0 )
            robust_scaler = RobustScaler()
            pipeline = pipeline(steps = [
                ('Imputer',simple_imputer),
                ('Robustscaler',robust_scaler)
            ])
            return pipeline
            
        except Exception as e:
            raise InsuraneceException(e,sys)
    
    def initiate_data_transformation(self,)->artifact_entity.DataTransformationArtifact:
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            input_feature_train_df = train_df.drop(TARGET_COLUMN,axis = 1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN,axis = 1)

            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            label_encoder = LabelEncoder()
            ## fit data
            target_feature_train_arr = target_feature_train_df.squeeze()
            target_feature_test_arr = target_feature_test_df.squeeze()

            for col in input_feature_train_df.columns:
                if in


        except Exception as e:
            raise InsuraneceException(e,sys)


