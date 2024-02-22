import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from logger import logging



class Preprocessor:
    def __init__(self):
        pass

    def remove_columns(self,data,columns):
        
        logging.info('Entered the remove_columns method of the Preprocessor class')
        try:
            useful_data=data.drop(labels=columns, axis=1) # drop the labels specified in the columns
            logging.info(str(columns) + 'Column removal Successful. Exited the remove_columns method of the Preprocessor class')
            return useful_data
        
        except Exception as e:
            logging.info('Exception occured in remove_columns method of the Preprocessor class. Exception message:  '+str(e))
            logging.info('Column removal Unsuccessful. Exited the remove_columns method of the Preprocessor class')
            logging.info(e)
            raise e

    def separate_label_feature(self, data, label_column_name):
        try:
            logging.info('Entered the separate_label_feature method of the Preprocessor class')
            data = data.rename(columns={'Good/Bad': 'Output'})
            X=data.drop(columns=label_column_name,axis=1) # drop the columns specified and separate the feature columns
            Y=data[label_column_name] # Filter the Label columns
            logging.info('Label Separation Successful. Exited the separate_label_feature method of the Preprocessor class')
            return X,Y
        except Exception as e:
            logging.exception('Exception occured in separate_label_feature method of the Preprocessor class. Exception message:  ' + str(e))
            logging.exception( 'Label Separation Unsuccessful. Exited the separate_label_feature method of the Preprocessor class')
            logging.exception(e)
            raise e

    def is_null_present(self,data): #this will check if null values
        logging.info('Entered the is_null_present method of the Preprocessor class')
        null_present = False
        try:
            null_counts=data.isna().sum() # check for the count of null values per column
            for i in null_counts:
                if i>0:
                    null_present=True
                    break

            if(null_present): # write the logs to see which columns have null values
                dataframe_with_null = pd.DataFrame()
                dataframe_with_null['columns'] = data.columns
                dataframe_with_null['missing values count'] = np.asarray(data.isna().sum())
                dataframe_with_null.to_csv('preprocessing_data/null_values.csv') # storing the null column information to file
            
            logging.info('Finding missing values is a success.Data written to the null values file. Exited the is_null_present method of the Preprocessor class')
            return null_present
        except Exception as e:
            logging.exception('Exception occured in is_null_present method of the Preprocessor class. Exception message:  ' + str(e))
            logging.exception('Finding missing values failed. Exited the is_null_present method of the Preprocessor class')
            raise e

    def impute_missing_values(self, data):
        logging.info( 'Entered the impute_missing_values method of the Preprocessor class')
        try:
            column_names = data.columns
            imputer=KNNImputer(n_neighbors=3, weights='uniform',missing_values=np.nan) # we are using KNN imputer
            new_array=imputer.fit_transform(data) # impute the missing values
            # convert the nd-array returned in the step above to a Dataframe
            new_data=pd.DataFrame(data=new_array, columns=column_names)
            logging.info('Imputing missing values Successful. Exited the impute_missing_values method of the Preprocessor class')
            return new_data
        except Exception as e:
            logging.exception('Exception occured in impute_missing_values method of the Preprocessor class. Exception message:  ' + str(e))
            logging.exception('Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class')
            logging.exception(e)
            raise e

    def get_columns_with_zero_std_deviation(self,data):
        logging.info( 'Entered the get_columns_with_zero_std_deviation method of the Preprocessor class')
        columns=data.columns
        data_n = data.describe()
        col_to_drop=[]
        try:
            for x in columns:
                if (data_n[x]['std'] == 0): # check if standard deviation is zero
                    col_to_drop.append(x)  # prepare the list of columns with standard deviation zero
            logging.info( 'Column search for Standard Deviation of Zero Successful. Exited the get_columns_with_zero_std_deviation method of the Preprocessor class')
            return col_to_drop

        except Exception as e:
            logging.exception('Exception occured in get_columns_with_zero_std_deviation method of the Preprocessor class. Exception message:  ' + str(e))
            logging.exception('Column search for Standard Deviation of Zero Failed. Exited the get_columns_with_zero_std_deviation method of the Preprocessor class')
            logging.exception(e)
            raise e