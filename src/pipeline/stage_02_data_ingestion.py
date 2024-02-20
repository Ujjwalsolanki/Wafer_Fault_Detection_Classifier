from src.components.data_ingestion import DataIngestion
from logger import get_logger


STAGE_NAME = "Data ingestion - Creating a master data files"

class DataIngestionTrainingPipeline:
    def __init__(self):
        self.logger = get_logger()

    def main(self):
        self.logger.info("data ingestion created")
        data_ingestion = DataIngestion()
        data_ingestion.create_master_data_file()


if __name__ == '__main__':
    try:
        logger = get_logger()
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

