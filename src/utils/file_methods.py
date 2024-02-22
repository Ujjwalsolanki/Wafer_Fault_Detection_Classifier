import os
from box import ConfigBox
from box.exceptions import BoxValueError
import yaml
from logger import logging
import json
import joblib
import pickle
import os
import shutil
from ensure import ensure_annotations
from pathlib import Path
from typing import Any


class FileOperations:
    def __init__(self) -> None:
        pass

    @ensure_annotations
    def read_yaml(self, path_to_yaml: Path) -> ConfigBox:
        """reads yaml file and returns

        Args:
            path_to_yaml (str): path like input

        Raises:
            ValueError: if yaml file is empty
            e: empty file

        Returns:
            ConfigBox: ConfigBox type
        """
        try:
            with open(path_to_yaml) as yaml_file:
                content = yaml.safe_load(yaml_file)
                logging.info(f"yaml file: {path_to_yaml} loaded successfully")
                return ConfigBox(content)
        except BoxValueError:
            raise ValueError("yaml file is empty")
        except Exception as e:
            raise e
        


    @ensure_annotations
    def create_directories(self, path_to_directories: list, verbose=True):
        """create list of directories

        Args:
            path_to_directories (list): list of path of directories
            ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
        """
        for path in path_to_directories:
            os.makedirs(path, exist_ok=True)
            if verbose:
                logging.info(f"created directory at: {path}")


    @ensure_annotations
    def save_json(self, path: Path, data: dict):
        """save json data

        Args:
            path (Path): path to json file
            data (dict): data to be saved in json file
        """
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        logging.info(f"json file saved at: {path}")


    @ensure_annotations
    def load_json(self, path: Path) -> ConfigBox:
        """load json files data

        Args:
            path (Path): path to json file

        Returns:
            ConfigBox: data as class attributes instead of dict
        """
        with open(path) as f:
            content = json.load(f)

        logging.info(f"json file loaded succesfully from: {path}")
        return ConfigBox(content)


    @ensure_annotations
    def save_bin(self, data: Any, path: Path):
        """save binary file

        Args:
            data (Any): data to be saved as binary
            path (Path): path to binary file
        """
        joblib.dump(value=data, filename=path)
        logging.info(f"binary file saved at: {path}")


    @ensure_annotations
    def load_bin(self, path: Path) -> Any:
        """load binary data

        Args:
            path (Path): path to binary file

        Returns:
            Any: object stored in the file
        """
        data = joblib.load(path)
        logging.info(f"binary file loaded from: {path}")
        return data



    @ensure_annotations
    def get_size(self, path: Path) -> str:
        """get size in KB

        Args:
            path (Path): path of the file

        Returns:
            str: size in KB
        """
        size_in_kb = round(os.path.getsize(path)/1024)
        return f"~ {size_in_kb} KB"
    

    def save_model(self, model, path, filename):
        logging.info('Entered the save_model method of the File_Operation class')
        try:
            path = os.path.join(path,filename) #create seperate directory for each cluster
            if os.path.isdir(path): #remove previously existing models for each clusters
                shutil.rmtree(path)
                os.makedirs(path)
            else:
                os.makedirs(path) #
            with open(path +'/' + filename+'.sav', 'wb') as f:
                pickle.dump(model, f) # save the model to file
            logging.info('Model File '+filename+' saved. Exited the save_model method of the Model_Finder class')

            return True
        except Exception as e:
            logging.exception('Exception occured in save_model method of the Model_Finder class. Exception message:  ' + str(e))
            logging.exception('Model File '+filename+' could not be saved. Exited the save_model method of the Model_Finder class')
            raise Exception()

    def load_model(self,filename):
        logging.info(self.file_object, 'Entered the load_model method of the File_Operation class')
        try:
            with open(self.model_directory + filename + '/' + filename + '.sav', 'rb') as f:
                logging.info(self.file_object, 'Model File ' + filename + ' loaded. Exited the load_model method of the Model_Finder class')
                return pickle.load(f)
        except Exception as e:
            logging.exception('Exception occured in load_model method of the Model_Finder class. Exception message:  ' + str(e))
            logging.exception('Model File ' + filename + ' could not be saved. Exited the load_model method of the Model_Finder class')
            raise Exception()

    def find_correct_model_file(self,cluster_number):
        logging.info('Entered the find_correct_model_file method of the File_Operation class')
        try:
            self.cluster_number= cluster_number
            self.folder_name=self.model_directory
            self.list_of_model_files = []
            self.list_of_files = os.listdir(self.folder_name)
            for self.file in self.list_of_files:
                try:
                    if (self.file.index(str( self.cluster_number))!=-1):
                        self.model_name=self.file
                except:
                    continue
            self.model_name=self.model_name.split('.')[0]
            logging.info('Exited the find_correct_model_file method of the Model_Finder class.')
            return self.model_name
        except Exception as e:
            logging.exception('Exception occured in find_correct_model_file method of the Model_Finder class. Exception message:  ' + str(e))
            logging.exception('Exited the find_correct_model_file method of the Model_Finder class with Failure')
            raise Exception()


