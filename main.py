from Insurance_Project.logger import logging
from Insurance_Project.exception import InsuraneceException
import os,sys
from Insurance_Project.utils import get_collecttion_as_dataframe
from Insurance_Project.entity.config_entity import DataIngestionConfig
from Insurance_Project.entity import config_entity
from Insurance_Project.components.data_ingestion import DataIngestion
from Insurance_Project.components.data_validation import Datavalidation


#def test_logger_and_exception():
    #try:
        #logging.info("Starting the test_logger_and_exception")
        #result = 3/0
        #print(result)    
        #logging.info("Ending point of the test_logger_and_exception")
    #except Exception as e:
        #logging.debug(str(e))
        #raise InsuraneceException(e,sys)

if __name__== "__main__":
    try:
        #get_collecttion_as_dataframe(database_name = "INSURANCE2",collection_name = "INSURANCE_PROJECT2")
        training_pipeline_config = config_entity.TrainingPipelineconfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        
        # Data Validation
        data_validaton_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = Datavalidation(data_validation_config=data_validaton_config,
        data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()
    except Exception as e:
        raise InsuraneceException(e,sys)