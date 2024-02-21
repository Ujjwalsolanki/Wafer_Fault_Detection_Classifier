
import os
import shutil
import pandas as pd
from src.utils.file_methods import FileOperations
from src.config.configuration import DataIngestionConfig
from logger import logging


class DataIngestion():
    def __init__(self) -> None:
        self.data_ingestion_config = DataIngestionConfig()

    def create_master_data_file(self):
        try:
            good_raw_file_path = os.path.join(self.data_ingestion_config.good_raw_data_path)
            good_files = [f for f in os.listdir(good_raw_file_path)]
            if good_files:
                df_list = []
                for file_name in good_files:
                    csv = pd.read_csv(good_raw_file_path +'/'+ file_name)
                    df_list.append(csv)

                master_df = pd.concat(df_list, ignore_index=True)

                master_df.to_csv("artifacts/data.csv", index=False)

                # delete validated files folder once we retrive our master file
                self.delete_validated_files()


            else:
                logging.exception("No good data files found")
                raise(Exception)
        except Exception as e:
            logging.exception(e)
            raise(e)
        
    def delete_validated_files(self):
        try:
            path = self.data_ingestion_config.validated_files_path
            if os.path.isdir(path):
                shutil.rmtree(path)
                logging.info("validated files folder deleted")
        except OSError as s:
            logging.info("Error while Deleting Directory : %s" %s)
            raise OSError
