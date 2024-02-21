from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataValidationConfig:
    raw_data_path:Path = Path('training_files')
    schema_file:Path = Path('schema.yaml')

@dataclass(frozen=True)
class DataIngestionConfig:
    good_raw_data_path:Path = Path('validated_files/good/')
    data_path:Path = Path('artifacts/data_csv')
    validated_files_path = Path('validated_files/')

@dataclass(frozen=True)
class DataLoaderConfig:
    data_path:Path = Path('artifacts/data.csv')