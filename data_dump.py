import pymongo
import pandas as pd
import json


client = pymongo.MongoClient("mongodb+srv://se2zT5RUfhSvQmau:se2zT5RUfhSvQmau@cluster0.8peshl5.mongodb.net/?retryWrites=true&w=majority")
db = client.test


DATA_FILE_PATH = (r"E:\ML_complete_project\insurance.csv")
DATBASE_NAME = "INSURANCE2"
COLLECTION_NAME = "INSURANCE_PROJECT2"

if __name__ == "__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and Columns: {df.shape}")

    df.reset_index(drop=True,inplace=True) ## dropping the index

    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])
    client[DATBASE_NAME][COLLECTION_NAME].insert_many(json_record)