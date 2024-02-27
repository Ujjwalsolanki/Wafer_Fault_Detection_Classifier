from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from logger import logging
from xgboost import XGBClassifier
from sklearn.metrics  import roc_auc_score,accuracy_score
from sklearn.preprocessing import LabelEncoder

class Model_Finder:
    def __init__(self):
        self.clf = RandomForestClassifier()
        self.xgb = XGBClassifier(objective='binary:logistic')

    def get_best_params_for_random_forest(self,X_train,y_train):
        try:
            logging.info( 'Entered the get_best_params_for_random_forest method of the Model_Finder class')
            # initializing with different combination of parameters
            param_grid = {
                "n_estimators": [10, 50, 100, 130],
                "criterion": ['gini', 'entropy'],
                "max_depth": range(2, 4, 1),
                "max_features": ['sqrt', 'log2']
            }

            #Creating an object of the Grid Search class
            grid = GridSearchCV(estimator=self.clf, param_grid=param_grid, cv=5, verbose=3)
            #finding the best parameters
            grid.fit(X_train,y_train)

            #extracting the best parameters
            criterion = grid.best_params_['criterion']
            max_depth = grid.best_params_['max_depth']
            max_features = grid.best_params_['max_features']
            n_estimators = grid.best_params_['n_estimators']

            #creating a new model with the best parameters
            clf = RandomForestClassifier(
                n_estimators=n_estimators,
                criterion=criterion,
                max_depth=max_depth,
                max_features=max_features
            )
            # training the mew model
            clf.fit(X_train,y_train)
            logging.info('Random Forest best params: '+str(grid.best_params_)+'. Exited the get_best_params_for_random_forest method of the Model_Finder class')

            return clf
        except Exception as e:
            logging.info('Exception occured in get_best_params_for_random_forest method of the Model_Finder class. Exception message:  ' + str(e))
            logging.info('Random Forest Parameter tuning  failed. Exited the get_best_params_for_random_forest method of the Model_Finder class')
            raise e

    def get_best_params_for_xgboost(self,X_train,y_train):
        try:
            logging.info('Entered the get_best_params_for_xgboost method of the Model_Finder class')
            le = LabelEncoder()
            y_train = le.fit_transform(y_train)
            # initializing with different combination of parameters
            param_grid_xgboost = {
                'learning_rate': [0.5, 0.1, 0.01, 0.001],
                'max_depth': [3, 5, 10, 20],
                'n_estimators': [10, 50, 100, 200]
            }

            # Creating an object of the Grid Search class
            grid= GridSearchCV(self.xgb,param_grid_xgboost, verbose=3,cv=5)
            # finding the best parameters
            grid.fit(X_train,y_train)

            # extracting the best parameters
            learning_rate = grid.best_params_['learning_rate']
            max_depth = grid.best_params_['max_depth']
            n_estimators = grid.best_params_['n_estimators']

            # creating a new model with the best parameters
            xgb = XGBClassifier(objective='binary:logistic',learning_rate=learning_rate, max_depth=max_depth, n_estimators=n_estimators)
            # training the mew model
            xgb.fit(X_train,y_train)
            logging.info('XGBoost best params: ' + str(grid.best_params_) + 
                         '. Exited the get_best_params_for_xgboost method of the Model_Finder class')
            return xgb
        except Exception as e:
            logging.info('Exception occured in get_best_params_for_xgboost method of the Model_Finder class. Exception message:  ' + str(e))
            logging.info('XGBoost Parameter tuning  failed. Exited the get_best_params_for_xgboost method of the Model_Finder class')
            raise e


    def get_best_model(self,X_train, X_test, y_train, y_test):
        logging.info('Entered the get_best_model method of the Model_Finder class')
        # create best model for XGBoost
        try:
            xgboost= self.get_best_params_for_xgboost(X_train,y_train)
            prediction_xgboost = xgboost.predict(X_test) # Predictions using the XGBoost Model

            if len(y_test.unique()) == 1: #if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                xgboost_score = accuracy_score(y_test, prediction_xgboost)
                logging.info( 'Accuracy for XGBoost:' + str(xgboost_score))  # Log AUC
            else:
                xgboost_score = roc_auc_score(y_test, prediction_xgboost) # AUC for XGBoost
                logging.info( 'AUC for XGBoost:' + str(xgboost_score)) # Log AUC

            # create best model for Random Forest
            random_forest=self.get_best_params_for_random_forest(X_train, y_train)
            prediction_random_forest=random_forest.predict(X_test) # prediction using the Random Forest Algorithm

            if len(y_test.unique()) == 1:#if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                random_forest_score = accuracy_score(y_test,prediction_random_forest)
                logging.info( 'Accuracy for RF:' + str(random_forest_score))
            else:
                random_forest_score = roc_auc_score(y_test, prediction_random_forest) # AUC for Random Forest
                logging.info( 'AUC for RF:' + str(random_forest_score))

            #comparing the two models
            if(random_forest_score <  xgboost_score):
                return 'XGBoost',xgboost
            else:
                return 'RandomForest',random_forest

        except Exception as e:
            logging.info('Exception occured in get_best_model method of the Model_Finder class. Exception message:  ' + str(e))
            logging.info('Model Selection Failed. Exited the get_best_model method of the Model_Finder class')
            raise e

