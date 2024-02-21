import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.cluster import KMeans
from kneed import KneeLocator

from src.utils.file_methods import FileOperations
from logger import logging

class KMeansClustering:
    def __init__(self):
        pass

    def elbow_plot(self,data):
        
        logging.info('Entered the elbow_plot method of the KMeansClustering class')
        wcss=[] # initializing an empty list
        try:
            # based on different experiment 50 and up gives same knee == 8
            for i in range (1,50):
                kmeans=KMeans(n_clusters=i,init='k-means++',random_state=30) # initializing the KMeans object
                kmeans.fit(data) # fitting the data to the KMeans Algorithm
                wcss.append(kmeans.inertia_)

            plt.plot(range(1,50),wcss) # creating the graph between WCSS and the number of clusters
            plt.title('The Elbow Method')
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')
            #plt.show()

            plt.savefig('preprocessing_data/K-Means_Elbow.PNG') # saving the elbow plot locally
            
            # finding the value of the optimum cluster programmatically
            knee_locator = KneeLocator(range(1, 50), wcss, curve='convex', direction='decreasing')
            logging.info('The optimum number of clusters is: '+str(knee_locator.knee)+' . Exited the elbow_plot method of the KMeansClustering class')
            return knee_locator.knee

        except Exception as e:
            logging.exception('Exception occured in elbow_plot method of the KMeansClustering class. Exception message:  ' + str(e))
            logging.exception('Finding the number of clusters failed. Exited the elbow_plot method of the KMeansClustering class')
            logging.exception(e)
            raise Exception()

    def create_clusters(self,data,number_of_clusters):
        logging.info('Entered the create_clusters method of the KMeansClustering class')
        try:
            path = Path('artifacts/models')
            kmeans = KMeans(n_clusters=number_of_clusters, init='k-means++', random_state=30)
            #self.data = self.data[~self.data.isin([np.nan, np.inf, -np.inf]).any(1)]
            y_kmeans=kmeans.fit_predict(data) #  divide data into clusters

            file_operations = FileOperations()
            save_model = file_operations.save_model(kmeans, path,  'KMeans') # saving the KMeans model to directory
            
            data['Cluster']=y_kmeans  # create a new column in dataset for storing the cluster information
            logging.info('succesfully created clusters. Exited the create_clusters method of the KMeansClustering class')
            return data                                                                        # passing 'Model' as the functions need three parameters

        except Exception as e:
            logging.info('Exception occured in create_clusters method of the KMeansClustering class. Exception message:  ' + str(e))
            logging.info('Fitting the data to clusters failed. Exited the create_clusters method of the KMeansClustering class')
            raise Exception(e)