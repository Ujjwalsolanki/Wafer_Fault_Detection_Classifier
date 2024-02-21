from src.components.data_ingestion import DataIngestion


class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        data_ingestion = DataIngestion()
        data_ingestion.create_master_data_file()


if __name__ == '__main__':
    try:
        obj = DataIngestionTrainingPipeline()
        obj.main()
    except Exception as e:
        raise e

