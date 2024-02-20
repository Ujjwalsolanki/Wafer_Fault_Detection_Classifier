from src.pipeline.stage_01_data_validation import DataValidationTrainingPipeline
from logger import get_logger

STAGE_NAME = "Data Validation stage"

if __name__ == '__main__':
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
