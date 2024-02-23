from datetime import datetime
from os import listdir
import os
from pathlib import Path
import re
from logger import logging
import shutil
import pandas as pd

from src.utils.file_methods import FileOperations


class PredictionDataValidation:

    def __init__(self,path):
        self.path = path
        self.schema_path = Path('prediction_schema.yaml')


    def get_values_from_schema_file(self):
        
        try:
            file_op = FileOperations()
            schema = file_op.read_yaml(self.schema_path)

            length_of_date_stamp = schema.LengthOfDateStampInFile
            length_of_time_stamp = schema.LengthOfTimeStampInFile
            column_names = schema.ColName
            number_of_columns = schema.NumberOfColumns

            message = ("length_of_date_stamp:: %s" % length_of_date_stamp + "\t" + "length_of_time_stamp:: %s" %
                       length_of_time_stamp + "\t " + "number_of_columns:: %s" % number_of_columns)
            logging.info(message)

            return length_of_date_stamp, length_of_time_stamp, column_names, number_of_columns

        except ValueError:
            logging.exception("ValueError:Value not found inside schema_training.json")
            raise ValueError

        except KeyError:
            logging.exception( "KeyError:Key value error incorrect key passed")
            raise KeyError

        except Exception as e:
            logging.exception(e)
            raise e

    def createDirectoryForGoodBadPredData(self):

        try:
            path = os.path.join("prediction_raw_files_validated/", "good/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join("prediction_raw_files_validated/", "bad/")
            if not os.path.isdir(path):
                os.makedirs(path)

        except OSError as e:
            logging.exception("Error while creating Directory %s:" % e)
            raise OSError

    def deleteExistingGoodDataPredFolder(self):
        
        try:
            path = 'prediction_raw_files_validated/'
            if os.path.isdir(path + 'good/'):
                shutil.rmtree(path + 'good/')
                logging.info("GoodRaw directory deleted successfully!!!")
        except OSError as s:
            logging.exception("Error while Deleting Directory : %s" %s)
            raise OSError
        
    def deleteExistingBadDataPredFolder(self):

        try:
            path = 'prediction_raw_files_validated/'
            if os.path.isdir(path + 'bad/'):
                shutil.rmtree(path + 'bad/')
                logging.info("BadRaw directory deleted before starting validation!!!")
        except OSError as s:
            logging.exception("Error while Deleting Directory : %s" %s)
            raise OSError

    def moveBadFilesToArchiveBad(self):

        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        try:
            path= "PredictionArchivedBadData"
            if not os.path.isdir(path):
                os.makedirs(path)
            source = 'prediction_raw_files_validated/bad/'
            dest = 'PredictionArchivedBadData/BadData_' + str(date)+"_"+str(time)
            if not os.path.isdir(dest):
                os.makedirs(dest)
            files = os.listdir(source)
            for f in files:
                if f not in os.listdir(dest):
                    shutil.move(source + dest)
            file = open("Prediction_Logs/GeneralLog.txt", 'a+')
            logging.info("Bad files moved to archive")
            path = 'prediction_raw_files_validated/'
            if os.path.isdir(path + 'bad/'):
                shutil.rmtree(path + 'bad/')
            logging.info("Bad Raw Data Folder Deleted successfully!!")
            file.close()
        except OSError as e:
            file = open("Prediction_Logs/GeneralLog.txt", 'a+')
            logging.info( "Error while moving bad files to archive:: %s" % e)
            file.close()
            raise OSError


    def validate_file_name(self,length_of_date_stamp, length_of_time_stamp):
        
        regex = "['wafer']+['\_'']+[\d_]+[\d]+\.csv"
        # delete the directories for good and bad data in case last run was unsuccessful and folders were not deleted.
        self.deleteExistingBadDataPredFolder()
        self.deleteExistingGoodDataPredFolder()
        self.createDirectoryForGoodBadPredData()
        files = [f for f in listdir(self.path)]
        try:
            for filename in files:
                if (re.match(regex, filename)):
                    splitAtDot = re.split('.csv', filename)
                    splitAtDot = (re.split('_', splitAtDot[0]))
                    if len(splitAtDot[1]) == length_of_date_stamp:
                        if len(splitAtDot[2]) == length_of_time_stamp:
                            shutil.copy(self.path +"/"+ filename, "prediction_raw_files_validated/good/")
                            logging.info("Valid File name!! File moved to GoodRaw Folder :: %s" % filename)

                        else:
                            shutil.copy(self.path +"/"+ filename, "prediction_raw_files_validated/bad/")
                            logging.warning("Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                    else:
                        shutil.copy(self.path+"/"+ filename, "prediction_raw_files_validated/bad/")
                        logging.warning("Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                else:
                    shutil.copy(self.path +"/"+ filename, "prediction_raw_files_validated/bad/")
                    logging.warning("Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)

        except Exception as e:
            logging.exception("Error occured while validating FileName %s" % e)
            raise e


    def validate_column_length(self,number_of_columns):
        
        try:
            logging.info("Column Length Validation Started!!")
            for file in listdir('prediction_raw_files_validated/good/'):
                csv = pd.read_csv("prediction_raw_files_validated/good/" + file)
                if csv.shape[1] == number_of_columns:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv("prediction_raw_files_validated/good/" + file ,  index=None, header=True)
                else:
                    shutil.move("prediction_raw_files_validated/good/" + file,  "prediction_raw_files_validated/bad/"+ file)
                    logging.info("Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)

            logging.info("Column Length Validation Completed!!")
        except OSError:
            logging.info("Error Occured while moving the file :: %s" % OSError)
            raise OSError
        except Exception as e:
            logging.info("Error Occured:: %s" % e)
            raise e

    def deletePredictionFile(self):

        if os.path.exists('Prediction_Output_File/Predictions.csv'):
            os.remove('Prediction_Output_File/Predictions.csv')

    def validate_missing_value_in_whole_column(self):
        
        try:
            logging.info("Missing Values Validation Started!!")

            for file in listdir('prediction_raw_files_validated/good/'):
                csv = pd.read_csv("prediction_raw_files_validated/good/" + file)
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count+=1
                        shutil.move("prediction_raw_files_validated/good/" + file,
                                    "prediction_raw_files_validated/bad/" + file)
                        logging.info("Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
                        break
                if count==0:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv("prediction_raw_files_validated/good/" + file, index=None, header=True)
        except OSError:
            logging.info("Error Occured while moving the file :: %s" % OSError)
            raise OSError
        except Exception as e:
            logging.info("Error Occured:: %s" % e)
            raise e













