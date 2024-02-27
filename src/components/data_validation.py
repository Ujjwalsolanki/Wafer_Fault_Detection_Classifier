

import os
import re
import shutil
from ensure import ensure_annotations
import pandas as pd
from src.utils.file_methods import FileOperations
from src.config.configuration import DataValidationConfig
from logger import logging



class RowDataValidation:
    def __init__(self):
        self.data_validation_config = DataValidationConfig()
    
    def initiate_data_validation(self):
        try:
            logging.info("Data validation started")
            length_of_date_stamp, length_of_time_stamp, column_names, number_of_columns = self.get_values_from_schema_file()
        
            logging.info("File name validation started")
            self.validate_file_name(length_of_date_stamp, length_of_time_stamp)

            logging.info("Column length validation started")
            self.validate_column_length(number_of_columns)

            logging.info("Missing value validation started")
            self.validate_missing_values()

        except Exception as e:
            logging.exception(str(e))


    def get_values_from_schema_file(self):
        """
        here we can make assumption that all training file will follow pattern for the file name
        and feature details inside it.
        we can use
        length_of_date_stamp = 8
        length_of_time_stamp = 6
        column_names = wafer name, Wafer1 .... wafer590, output
        number_of_columns = 592
        :return:
        """
        try:
            file_op = FileOperations()
            schema = file_op.read_yaml(self.data_validation_config.schema_file)

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
            logging.exception("KeyError:Key value error incorrect key passed")
            raise KeyError

        except Exception as e:
            logging.exception(str(e))
            raise e

    @ensure_annotations
    def validate_file_name(self, length_of_date_stamp:int, length_of_time_stamp:int):

        regex = "['wafer']+['\_'']+[\d_]+[\d]+\.csv"

        # delete the directories for bad data in case last run was unsuccessful and folders were not deleted.
        self.delete_bad_data_file_folders()

        # delete the directories for good data in case last run was unsuccessful and folders were not deleted.
        self.delete_good_data_file_folders()
        # create new directories
        self.create_folders_good_data_bad_data()

        all_files = [f for f in os.listdir(self.data_validation_config.raw_data_path)]

        try:
            for filename in all_files:

                if re.match(regex, filename):
                    split_file_name = re.split('.csv', filename)
                    split_file_name = (re.split('_', split_file_name[0]))

                    if ((len(split_file_name[1]) == length_of_date_stamp) &
                            (len(split_file_name[2]) == length_of_time_stamp)):

                        shutil.copy("training_files/" + filename, "validated_files/good")
                        logging.info("Valid File name!! File moved to Good Files Folder :: %s" % filename)
                    else:
                        shutil.copy("training_files/" + filename, "validated_files/bad")
                        logging.info("Invalid File Name!! File moved to Bad Files Folder :: %s" % filename)
                else:
                    shutil.copy("training_files/" + filename, "validated_files/bad")
                    logging.info("Invalid File Name!! File moved to Bad Files Folder :: %s" % filename)

        except Exception as e:
            logging.info("Error occurred while validating FileName %s" % e)
            raise e

    def validate_column_length(self, number_of_columns: int):

        try:
            logging.info("Column Length Validation Started!!")

            for file in os.listdir('validated_files/good/'):
                csv = pd.read_csv("validated_files/good/" + file)

                # if length of columns names are not matching with schema file then we will reject this file,
                # Email Notification
                # pd.shape method will give us total rows and total columns in that file
                if csv.shape[1] != number_of_columns:
                    shutil.move("validated_files/good/" + file, "validated_files/bad")
                    logging.info("Invalid Column Length for the file!! File moved to Bad Files Folder :: %s" % file)

            logging.info("Column Length Validation Completed!!")

        except OSError:
            logging.info("Error Occurred while moving the file :: %s" % OSError)
            raise OSError

        except Exception as e:
            logging.info("Error Occurred:: %s" % e)
            raise e

    def create_folders_good_data_bad_data(self):
        try:
            os.makedirs("validated_files/", exist_ok=True)
            path = os.path.join("validated_files/", "good/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join("validated_files/", "bad/")
            if not os.path.isdir(path):
                os.makedirs(path)

        except OSError as ex:
            logging.exception("Error while creating Directory %s:" % ex)
            raise OSError

    def delete_bad_data_file_folders(self):
        try:
            path = 'validated_files/'
            if os.path.isdir(path + 'bad/'):
                shutil.rmtree(path + 'bad/')
                logging.info("Bad Files directory deleted before starting validation!!!")
        except OSError as s:
            logging.exception("Error while Deleting Directory : %s" % s)
            raise OSError

    def delete_good_data_file_folders(self):
        try:
            path = 'validated_files/'
            if os.path.isdir(path + 'good/'):
                shutil.rmtree(path + 'good/')
                logging.info("Good Files directory deleted before starting validation!!!")
        except OSError as s:
            logging.exception("Error while Deleting Directory : %s" % s)
            raise OSError

    def validate_missing_values(self):
        try:
            logging.info("Missing Values Validation Started!!")

            for file in os.listdir('validated_files/good/'):
                data = pd.read_csv("validated_files/good/" + file)
                count = 0
                for columns in data:
                    # if all the columns are empty then we will consider it as a bad file
                    if (len(data[columns]) - data[columns].count()) == len(data[columns]):
                        count += 1
                        shutil.move("validated_files/good/" + file,
                                    "validated_files/bad")
                        logging.info("Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
                        break
                if count == 0:
                    data.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    data.to_csv('validated_files/good/' + file, index=None, header=True)

        except OSError:
            logging.exception("Error Occurred while moving the file :: %s" % OSError)
            raise OSError
        except Exception as e:
            logging.exception("Error Occurred:: %s" % e)
            raise e
