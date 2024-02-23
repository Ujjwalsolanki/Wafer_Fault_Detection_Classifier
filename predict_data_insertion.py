import os
import pandas as pd
from datetime import datetime
from logger import logging
from pathlib import Path
from prediction.prediction_data_transform import PredictionDataTransform

from prediction.prediction_data_validation import PredictionDataValidation

class PredValidation:
    def __init__(self,path: Path):
        self.path = path
        self.pred_data_validation = PredictionDataValidation(path)
        self.pred_data_transform = PredictionDataTransform(path)

    def initiate_prediction_validation(self):

        try:

            logging.info('Start of Validation on files for prediction!!')
            #extracting values from prediction schema
            LengthOfDateStampInFile,LengthOfTimeStampInFile,column_names,noofcolumns = self.pred_data_validation.get_values_from_schema_file()
            #validating filename of prediction files
            self.pred_data_validation.validate_file_name(LengthOfDateStampInFile,LengthOfTimeStampInFile)
            #validating column length in the file
            self.pred_data_validation.validate_column_length(noofcolumns)
            #validating if any column has all values missing
            self.pred_data_validation.validate_missing_value_in_whole_column()
            logging.info("Raw Data Validation Complete!!")

            logging.info(("Starting Data Transforamtion!!"))
            #replacing blanks in the csv file with "Null" values to insert in table
            self.pred_data_transform.replace_missing_value_with_null()

            logging.info("DataTransformation Completed!!!")

            logging.info("Creating Prediction master file and tables on the basis of given schema!!!")
            self.create_master_data_file()

        except Exception as e:
            raise e



    def create_master_data_file(self):
        try:
            good_raw_file_path = 'prediction_raw_files_validated/good/'
            good_files = [f for f in os.listdir(good_raw_file_path)]
            if good_files:
                df_list = []
                for file_name in good_files:
                    csv = pd.read_csv(good_raw_file_path + file_name)
                    df_list.append(csv)

                master_df = pd.concat(df_list, ignore_index=True)

                master_df.to_csv("prediction/data.csv", index=False)

            else:
                logging.exception("No good data files found")
                raise(Exception)
        except Exception as e:
            logging.exception(e)
            raise(e)





