import os
from pathlib import Path
import pandas
from logger import logging

from prediction.prediction_data_loader import PredictionDataLoader
from preprocessing_data.preprocessing import Preprocessor
from src.utils.file_methods import FileOperations


class Prediction:

    def __init__(self,path):
        self.path = path

    def predict_from_model(self):

        try:
            logging.info("Prediction started")
            logging.info("Delete prev prediction files")
            self.delete_prediction_file() #deletes the existing prediction file from last run!

            data_getter=PredictionDataLoader()
            data=data_getter.get_data()

            #code change
            # wafer_names=data['Wafer']
            # data=data.drop(labels=['Wafer'],axis=1)

            preprocessor=Preprocessor()

            is_null_present=preprocessor.is_null_present(data)

            if(is_null_present):
                data=preprocessor.impute_missing_values(data)

            # cols_to_drop=preprocessor.get_columns_with_zero_std_deviation(data)

            # data=preprocessor.remove_columns(data,cols_to_drop)
            #data=data.to_numpy()
            file_loader=FileOperations()

            kmeans=file_loader.load_model('KMeans')

            X = data.drop(columns=['Wafer'],axis=1)

            #drops the first column for cluster prediction
            clusters=kmeans.predict(X)

            data['clusters']=clusters

            clusters=data['clusters'].unique()

            for i in clusters:
                cluster_data= data[data['clusters']==i]
                wafer_names = list(cluster_data['Wafer'])
                cluster_data=data.drop(columns=['Wafer'],axis=1)
                cluster_data = cluster_data.drop(['clusters'],axis=1)
                model_name = file_loader.find_correct_model_file(i)
                model = file_loader.load_model(model_name)
                result=list(model.predict(cluster_data))
                result = pandas.DataFrame(list(zip(wafer_names,result)),columns=['Wafer','Prediction'])
                path="prediction/prediction_output_files/predictions.csv"
                result.to_csv("prediction/prediction_output_files/predictions.csv",header=True,mode='a+') #appends result to prediction file
            logging.info('End of Prediction')
            return path, result.head().to_json(orient="records")
        except Exception as e:
            logging.info('Error occured while running the prediction!! Error:: %s' % e)
            raise e

    def delete_prediction_file(self):
        try:
            prediction_directory = 'prediction_output_files/'

            if os.path.exists(prediction_directory + 'predictions.csv'):
                os.remove(prediction_directory + 'predictions.csv')
        except Exception as e:
            raise e