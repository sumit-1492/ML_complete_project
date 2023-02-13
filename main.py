from Insurance_Project.logger import logging
from Insurance_Project.exception import InsuraneceException
import os,sys
from Insurance_Project.utils import get_collecttion_as_dataframe

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
        get_collecttion_as_dataframe(database_name = "INSURANCE2",collection_name = "INSURANCE_PROJECT2")
    except Exception as e:
        print(e)