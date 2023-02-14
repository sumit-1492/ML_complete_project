import pandas as pd
import numpy as np
import os,sys
from Insurance_Project.entity import config_entity
from Insurance_Project.entity import artifact_entity
from Insurance_Project.exception import InsuraneceException
from Insurance_Project import utils
from Insurance_Project.logger import logging
from sklearn.model_selection import train_test_split

class DataIngestion: ## data divided into train,test,validate
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            InsuraneceException(e,sys)
    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        ##data collection
        try:
            logging.info(f"export data as pandas datframe")
            df:pd.DataFrame = utils.get_collecttion_as_dataframe(
                database_name   = self.data_ingestion_config.database_name,
                collection_name = self.data_ingestion_config.collection_name
            )
            logging.info(f"Save data in future store")

            ## replacing with nan
            df.replace(to_replace="na",value=np.NAN,inplace = True)
            
            ## save data in future store
            logging.info("Create feature store folder if not availabel")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok = True)
            logging.info("Save df to feature store folder")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False)

            ### dividing train test split
            logging.info("Splitiing dataset into train and test set")
            train_df,test_df = train_test_split(df,test_size = self.data_ingestion_config.test_size,random_state = 1)

            logging.info("Craete dataset directory folder if not exist")
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info("Save ddatset to required folder")
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header = True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header = True)

            ### prepare artifact folder
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path = self.data_ingestion_config.feature_store_file_path,
                train_file_path = self.data_ingestion_config.train_file_path,
                test_file_path = self.data_ingestion_config.test_file_path
            )

        except Exception as e:
            raise InsuraneceException(e,sys)


