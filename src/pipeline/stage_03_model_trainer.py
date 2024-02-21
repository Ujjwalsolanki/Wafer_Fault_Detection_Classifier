
from src.components.model_trainer import TrainModel


class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        trainer = TrainModel()
        trainer.initiate_model_training()


if __name__ == '__main__':
    try:
        obj = ModelTrainingPipeline()
        obj.main()
    except Exception as e:
        raise e

