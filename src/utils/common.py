import os
from box import ConfigBox
from box.exceptions import BoxValueError
import yaml
from logger import get_logger
import json
import joblib
from ensure import ensure_annotations
from pathlib import Path
from typing import Any


class CommonClass:
    def __init__(self) -> None:
        self.logger = get_logger()


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
                self.logger.info(f"yaml file: {path_to_yaml} loaded successfully")
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
                self.logger.info(f"created directory at: {path}")


    @ensure_annotations
    def save_json(self, path: Path, data: dict):
        """save json data

        Args:
            path (Path): path to json file
            data (dict): data to be saved in json file
        """
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        self.logger.info(f"json file saved at: {path}")


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

        self.logger.info(f"json file loaded succesfully from: {path}")
        return ConfigBox(content)


    @ensure_annotations
    def save_bin(self, data: Any, path: Path):
        """save binary file

        Args:
            data (Any): data to be saved as binary
            path (Path): path to binary file
        """
        joblib.dump(value=data, filename=path)
        self.logger.info(f"binary file saved at: {path}")


    @ensure_annotations
    def load_bin(self, path: Path) -> Any:
        """load binary data

        Args:
            path (Path): path to binary file

        Returns:
            Any: object stored in the file
        """
        data = joblib.load(path)
        self.logger.info(f"binary file loaded from: {path}")
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
    




