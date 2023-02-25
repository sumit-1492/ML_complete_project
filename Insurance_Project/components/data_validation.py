from Insurance_Project.entity import artifact_entity,config_entity
from Insurance_Project.logger import logging
from Insurance_Project.exception import InsuraneceException
import pandas as pd
import numpy as np
from typing import Optional
import os,sys
from scipy.stats import ks_2samp
from Insurance_Project import config
from Insurance_Project import utils

class Datavalidation:
    def __init__(self,
                    data_validation_config:config_entity.DataValidationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:

            logging.info(f"******Data Validation************")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()
        except Exception as e:
            raise InsuraneceException(e,sys)


    def drop_mising_values_column(self, df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:
        try:
            threshold = self.data_validation_config.missing_threshold
            null_report = df.isna().sum() / df.shape[0]
            drop_columns_names = null_report[null_report>threshold].index

            self.validation_error[report_key_name] = list(drop_columns_names)
            df.drop(list(drop_columns_names),axis = 1, inplace=True)

            ### returns none if no column left
            if len(df.columns) == 0:
                return None
            return df
        except Exception as e:
            raise InsuraneceException(e,sys)

    def is_required_columns_exists(self, base_df:pd.DataFrame, current_df:pd.DataFrame, report_key_name:str)->bool:
        try:
            ## base data
            base_columns    = base_df  ## original insurance data
            current_columns = current_df ## data in artifact folder

            missing_columns = []
            for column in base_columns:
                if column not in current_columns:
                    logging.info(f"Columns: [{column} is not avilabel.]")
                    missing_columns.append(column)
            if len(missing_columns)>0:
                self.validation_error[report_key_name] = missing_columns
                return False
            return True
        except Exception as e:
            raise InsuraneceException(e,sys)

    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):

        try:
            drift_report = dict()

            base_columns = base_df.columns
            current_columns = current_df.columns

            for column in base_columns:
                base_data,current_data = base_df[column],current_df[column]

                same_distribution = ks_2samp(base_data,current_data)

                if same_distribution.pvalue > 0.05:
                    ## Null hypothesis accepted
                    drift_report[column] = {
                        "pvalue" : float(same_distribution.pvalue),
                        "same_distribution" : True
                    }

                else:
                    drift_report[column] = {
                        "pvalue" : float(same_distribution.pvalue),
                        "same_distribution" : False
                    }
            self.validation_error[report_key_name] = drift_report
        except Exception as e:
            raise InsuraneceException(e,sys)

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na":np.nan},inplace=True)
            base_df = self.drop_mising_values_column(df = base_df,report_key_name="Missing values within base dataset")

            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            train_df.replace({"na":np.nan},inplace=True)
            train_df = self.drop_mising_values_column(df = train_df,report_key_name="Missing values within train dataset")

            test_df.replace({"na":np.nan},inplace=True)
            test_df = self.drop_mising_values_column(df = test_df,report_key_name="Missing values within test dataset")

            exclude_columns = [config.TARGET_COLUMN]
            ## checking datatype of every dataframe
            base_df  = utils.convert_columns_float(df = base_df,exclude_columns=exclude_columns)
            train_df = utils.convert_columns_float(df = train_df,exclude_columns=exclude_columns)
            test_df  = utils.convert_columns_float(df = test_df,exclude_columns=exclude_columns)
            
            train_df_columns_status = self.is_required_columns_exists(base_df=base_df,
                                                current_df=train_df,report_key_name="Missing column in train dataset")
            test_df_columns_status = self.is_required_columns_exists(base_df=base_df,
                                                current_df=test_df,report_key_name="Missing column in train dataset")

            if train_df_columns_status:
                self.data_drift(base_df=base_df,current_df=train_df,report_key_name="data_drift_within_train_dataset")

            if test_df_columns_status:
                self.data_drift(base_df=base_df,current_df=test_df,report_key_name="data_drift_within_test_dataset")
            
            ### write your report
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,data= self.validation_error)
            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path,)
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            
            return data_validation_artifact
        except Exception as e:
            raise InsuraneceException(e,sys)

