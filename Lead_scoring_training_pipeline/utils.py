'''
filename: utils.py
functions: encode_features, get_train_model
creator: shashank.gupta
version: 1
'''

###############################################################################
# Import necessary modules
# ##############################################################################

import pandas as pd
import numpy as np

import sqlite3
from sqlite3 import Error

import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
import lightgbm as lgb
from sklearn.model_selection import train_test_split

from Lead_scoring_training_pipeline.constants import *
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score, precision_score, roc_curve
import matplotlib.pyplot as plt


###############################################################################
# Define the function to encode features
# ##############################################################################

def encode_features():
    '''
    This function one hot encodes the categorical features present in our  
    training dataset. This encoding is needed for feeding categorical data 
    to many scikit-learn models.

    INPUTS
        db_file_name : Name of the database file 
        db_path : path where the db file should be
        ONE_HOT_ENCODED_FEATURES : list of the features that needs to be there in the final encoded dataframe
        FEATURES_TO_ENCODE: list of features  from cleaned data that need to be one-hot encoded
       

    OUTPUT
        1. Save the encoded features in a table - features
        2. Save the target variable in a separate table - target


    SAMPLE USAGE
        encode_features()
        
    **NOTE : You can modify the encode_featues function used in heart disease's inference
        pipeline from the pre-requisite module for this.
    '''
    conn = sqlite3.connect(DB_PATH+DB_FILE_NAME)
    model_input_df = pd.read_sql('select * from model_input', conn)

    # create df to hold encoded data and intermediate data
    df_en = pd.DataFrame(columns=ONE_HOT_ENCODED_FEATURES)
    df_placeholder = pd.DataFrame()

    # encode the features using get_dummies()
    for f in FEATURES_TO_ENCODE:
        if(f in model_input_df.columns):
            encoded = pd.get_dummies(model_input_df[f])
            encoded = encoded.add_prefix(f + '_')
            df_placeholder = pd.concat([df_placeholder, encoded], axis=1)
        else:
            print('Feature not found')
            return model_input_df

    # add the encoded features into a single dataframe
    for feature in df_en.columns:
        if feature in model_input_df.columns:
            df_en[feature] = model_input_df[feature]
        if feature in df_placeholder.columns:
            df_en[feature] = df_placeholder[feature]
    df_en.fillna(0, inplace=True)

    # save the features and target in separate tables
    df_save_fea = df_en.drop(['app_complete_flag'], axis=1)
    df_save_tar = df_en[['app_complete_flag']]
    df_save_fea.to_sql(name='features', con=conn, if_exists='replace', index=False)
    df_save_tar.to_sql(name='target', con=conn, if_exists='replace', index=False)

    conn.close()



###############################################################################
# Define the function to train the model
# ##############################################################################

def get_trained_model():
    '''
    This function setups mlflow experiment to track the run of the training pipeline. It 
    also trains the model based on the features created in the previous function and 
    logs the train model into mlflow model registry for prediction. The input dataset is split
    into train and test data and the auc score calculated on the test data and
    recorded as a metric in mlflow run.   

    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be


    OUTPUT
        Tracks the run in experiment named 'Lead_Scoring_Training_Pipeline'
        Logs the trained model into mlflow model registry with name 'LightGBM'
        Logs the metrics and parameters into mlflow run
        Calculate auc from the test data and log into mlflow run  

    SAMPLE USAGE
        get_trained_model()
    '''
    # set the tracking uri and experiment
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT)

    # read the input data
    conn = sqlite3.connect(DB_PATH+DB_FILE_NAME)
    features_df = pd.read_sql('select * from features', conn)
    target_df = pd.read_sql('select * from target', conn)

    # split the dataset into train and test
    X_train, X_test, y_train, y_test = train_test_split(features_df, target_df, test_size=0.3, random_state=0)

    # start mlflow experiment
    with mlflow.start_run(run_name='run_LightGB') as mlrun:
        # train the model using LGBM Classifier on train dataset
        model = lgb.LGBMClassifier()
        model.set_params(**model_config)
        model.fit(X_train, y_train)

        # log model in mlflow model registry
        mlflow.sklearn.log_model(sk_model = model, artifact_path="models", registered_model_name='LightGBM')
        mlflow.log_params(model_config)

        # predict the results on test dataset
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]

        # Log metrics
        auc = roc_auc_score(y_test, y_pred_proba)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='binary')
        precision = precision_score(y_test, y_pred, average='binary')
        mlflow.log_metric('AUC', auc)
        mlflow.log_metric('Accuracy', acc)
        mlflow.log_metric('F1', f1)
        mlflow.log_metric('Precision', precision)
        print(f"AUC: {auc:.4f} | Accuracy: {acc:.4f} | F1: {f1:.4f} | Precision: {precision:.4f}")

        # Log ROC plot
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        plt.figure()
        plt.plot(fpr, tpr, label=f"AUC = {auc:.2f}")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("ROC Curve")
        plt.legend(loc="lower right")
        plot_path = "roc_curve.png"
        plt.savefig(plot_path)
        mlflow.log_artifact(plot_path)
        plt.close()
   
