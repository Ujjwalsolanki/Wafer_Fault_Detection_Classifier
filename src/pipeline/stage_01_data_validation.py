from src.components.data_validation import RowDataValidation


class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        data_validation = RowDataValidation()
        data_validation.initiate_data_validation()


if __name__ == '__main__':
    try:
        obj = DataValidationTrainingPipeline()
        obj.main()
    except Exception as e:
        raise e

