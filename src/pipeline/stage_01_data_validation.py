from src.components.data_validation import RowDataValidation
from logger import get_logger


STAGE_NAME = "Data Validation stage"

class DataValidationTrainingPipeline:
    def __init__(self):
        self.logger = get_logger()

    def main(self):
        data_validation = RowDataValidation()
        data_validation.initiate_data_validation()


if __name__ == '__main__':
    try:
        logger = get_logger()
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataValidationTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

