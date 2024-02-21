
import pandas as pd
from src.config.configuration import DataLoaderConfig
from logger import logging

class DataLoader():
    def __init__(self) -> None:
        self.data_loader_config = DataLoaderConfig()

    def get_data(self):
        try:
            logging.info('Entered the get_data method of the Data_Getter class')
            self.data = pd.read_csv(self.data_loader_config.data_path)
            logging.info('Data Load Successful.Exited the get_data method of the Data_Getter class')
            return self.data
        except Exception as e:
            logging.info('Exception occured in get_data method of the Data_Getter class. Exception message: '+str(e))
            logging.info('Data Load Unsuccessful.Exited the get_data method of the Data_Getter class')
            logging.exception(e)
            raise Exception()
