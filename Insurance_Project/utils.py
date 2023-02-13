import pandas as pd
import numpy as np
import os
import sys
from Insurance_Project.exception import InsuraneceException
from Insurance_Project.config import mongo_client
from Insurance_Project.logger import logging

def get_collecttion_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    try:
        logging.info(f"Reading data from Database:{database_name} and collection:{collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Find Columns:{df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping columns:_id")
            df = df.drop("_id",axis = 1)
        logging.info(f"Rows and columns in df: {df.shape}")
        return df

    except Exception as e:
        raise InsuraneceException(e,sys)
