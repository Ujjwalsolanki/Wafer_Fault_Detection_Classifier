from datetime import datetime
from os import listdir
from pathlib import Path
import pandas
from logger import logging
import pandas as pd


class PredictionDataTransform:

     
    def __init__(self, path: Path):
        self.path = Path("prediction_raw_files_validated/good/")


    def replace_missing_value_with_null(self):

        try:
            files = [f for f in listdir(self.path)]
            for file in files:
                csv = pd.read_csv("prediction_raw_files_validated/good/" + file)
                csv.fillna('NULL',inplace=True)
                csv['Wafer'] = csv['Wafer'].str[6:]
                csv.to_csv("prediction_raw_files_validated/good/" + file, index=None, header=True)
                logging.info(" %s: File Transformed successfully!!" % file)

        except Exception as e:
            logging.exception("Data Transformation failed because:: %s" % e)
            raise e
