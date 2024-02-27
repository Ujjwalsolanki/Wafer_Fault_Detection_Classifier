import pandas as pd
from logger import logging

class PredictionDataLoader:
    
    def __init__(self):
        self.prediction_file='Prediction/data.csv'

    def get_data(self):
        
        logging.info('Entered the get_data method of the Data_Getter class')
        try:
            self.data= pd.read_csv(self.prediction_file) # reading the data file
            logging.info('Data Load Successful.Exited the get_data method of the Data_Getter class')
            return self.data
        except Exception as e:
            logging.exception('Exception occured in get_data method of the Data_Getter class. Exception message: '+str(e))
            logging.exception('Data Load Unsuccessful.Exited the get_data method of the Data_Getter class')
            raise e


