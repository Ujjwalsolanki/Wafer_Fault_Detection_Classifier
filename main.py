from logger import get_logger
from src.pipeline.stage_01_data_validation import DataValidationTrainingPipeline
from src.pipeline.stage_02_data_ingestion import DataIngestionTrainingPipeline

STAGE_NAME = "Data Validation stage"

try:
    logger = get_logger()
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    obj = DataValidationTrainingPipeline()
    obj.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger = get_logger()
    logger.exception(e)
    raise e

STAGE_NAME = "Data Ingestion stage - Creating Master csv"

try:
    logger = get_logger()
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    obj = DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e