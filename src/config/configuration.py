from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class DataValidationConfig:
    raw_data_path:Path = Path('training_files')
    schema_file:Path = Path('schema.yaml')

@dataclass(frozen=True)
class DataIngestionConfig:
    pass