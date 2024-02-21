# Doing the necessary imports
from sklearn.model_selection import train_test_split

from src.components.data_loader import DataLoader
from preprocessing_data.preprocessing import Preprocessor
from preprocessing_data.clustering import KMeansClustering
from logger import logging

#Creating the common Logging object


class TrainModel:

    def __init__(self):
        pass

    def initiate_model_training(self):
        # Logging the start of Training
        logging.info('Start of Training')
        try:
            # Getting the data from the source
            data_loader=DataLoader()
            data=data_loader.get_data()


            """doing the data preprocessing"""

            preprocessor=Preprocessor()
            data=preprocessor.remove_columns(data,['Wafer']) # remove the unnamed column as it doesn't contribute to prediction.

            # create separate features and labels
            X,Y=preprocessor.separate_label_feature(data,label_column_name='Output')

            # check if missing values are present in the dataset
            is_null_present=preprocessor.is_null_present(X)

            # if missing values are there, replace them appropriately.
            if(is_null_present):
                X=preprocessor.impute_missing_values(X) # missing value imputation

            # check further which columns do not contribute to predictions
            # if the standard deviation for a column is zero, it means that the column has constant values
            # and they are giving the same output both for good and bad sensors
            # prepare the list of such columns to drop
            cols_to_drop=preprocessor.get_columns_with_zero_std_deviation(X)

            # drop the columns obtained above
            X=preprocessor.remove_columns(X,cols_to_drop)

            """ Applying the clustering approach"""

            kmeans=KMeansClustering() # object initialization.
            number_of_clusters=kmeans.elbow_plot(X)  #  using the elbow plot to find the number of optimum clusters

            # Divide the data into clusters
            X=kmeans.create_clusters(X,number_of_clusters)

            #create a new column in the dataset consisting of the corresponding cluster assignments.
            X['Labels']=Y

            # getting the unique clusters from our dataset
            list_of_clusters=X['Cluster'].unique()

            """parsing all the clusters and looking for the best ML algorithm to fit on individual cluster"""

            for i in list_of_clusters:
                cluster_data=X[X['Cluster']==i] # filter the data for one cluster

                # Prepare the feature and Label columns
                cluster_features=cluster_data.drop(['Labels','Cluster'],axis=1)
                cluster_label= cluster_data['Labels']

                # splitting the data into training and test set for each cluster one by one
                # x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1 / 3, random_state=355)

                # model_finder=tuner.Model_Finder(self.file_object,self.log_writer) # object initialization

                #getting the best model for each of the clusters
                # best_model_name,best_model=model_finder.get_best_model(x_train,y_train,x_test,y_test)

                #saving the best model to the directory.
                # file_op = file_methods.File_Operation(self.file_object,self.log_writer)
                # save_model=file_op.save_model(best_model,best_model_name+str(i))

            # logging the successful Training
            logging.info('Successful End of Training')

        except Exception as e:
            # logging the unsuccessful Training
            logging.exception('Unsuccessful End of Training')
            logging.exception(e)
            raise e