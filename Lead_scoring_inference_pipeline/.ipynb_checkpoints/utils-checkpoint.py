'''
filename: utils.py
functions: encode_features, load_model
creator: shashank.gupta
version: 1
'''

###############################################################################
# Import necessary modules
# ##############################################################################


import mlflow
import mlflow.sklearn
import pandas as pd

import sqlite3

import os
import logging

from datetime import datetime
from Lead_scoring_inference_pipeline.constants import *

###############################################################################
# Define the function to train the model
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
        **NOTE : You can modify the encode_featues function used in heart disease's inference
        pipeline for this.

    OUTPUT
        1. Save the encoded features in a table - features

    SAMPLE USAGE
        encode_features()
    '''
    conn = sqlite3.connect(DB_PATH+DB_FILE_NAME)
    model_input_df = pd.read_sql('select * from model_input', conn)

    # create df to hold encoded data and intermediate data
    df_en = pd.DataFrame(columns = ONE_HOT_ENCODED_FEATURES)
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
    df_en.to_sql(name='features_inference', con=conn, if_exists='replace', index=False)

    conn.close()

###############################################################################
# Define the function to load the model from mlflow model registry
# ##############################################################################

def get_models_prediction():
    '''
    This function loads the model which is in production from mlflow registry and 
    uses it to do prediction on the input dataset. Please note this function will the load
    the latest version of the model present in the production stage. 

    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be
        model from mlflow model registry
        model name: name of the model to be loaded
        stage: stage from which the model needs to be loaded i.e. production


    OUTPUT
        Store the predicted values along with input data into a table

    SAMPLE USAGE
        load_model()
    '''
    # set the tracking uri
    mlflow.set_tracking_uri(TRACKING_URI)

    # load the latest model from production stage
    loaded_model = mlflow.pyfunc.load_model(model_uri=f"models:/{MODEL_NAME}/{STAGE}")

    # read the new data
    conn = sqlite3.connect(DB_PATH+DB_FILE_NAME)
    df_fea_inf = pd.read_sql('select * from features_inference', conn)

    # run the model to generate the prediction on new data
    y_pred = loaded_model.predict(df_fea_inf)
    df_fea_inf['pred_app_complete_flag'] = y_pred

    # store the data in a table
    df_fea_inf.to_sql(name='predicted_values', con=conn, if_exists='replace', index=False)
    conn.close()

###############################################################################
# Define the function to check the distribution of output column
# ##############################################################################

def prediction_ratio_check():
    '''
    This function calculates the % of 1 and 0 predicted by the model and  
    and writes it to a file named 'prediction_distribution.txt'.This file 
    should be created in the ~/airflow/dags/Lead_scoring_inference_pipeline 
    folder. 
    This helps us to monitor if there is any drift observed in the predictions 
    from our model at an overall level. This would determine our decision on 
    when to retrain our model.
    

    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be

    OUTPUT
        Write the output of the monitoring check in prediction_distribution.txt with 
        timestamp.

    SAMPLE USAGE
        prediction_col_check()
    '''
    # read the input data
    conn = sqlite3.connect(DB_PATH+DB_FILE_NAME)
    df_pred_val = pd.read_sql('select * from predicted_values', conn)

    # get the distribution of categories in prediction col
    val_cnts = df_pred_val['pred_app_complete_flag'].value_counts(normalize=True)

    # write the output in a file
    ct = datetime.now()
    st = str(ct)+' %of 1 = ' + str(val_cnts[1])+' %of 2 ='+str(val_cnts[0])
    with open(FILE_PATH+'prediction_distribution.txt', 'a') as f:
        f.write(st+"\n")

###############################################################################
# Define the function to check the columns of input features
# ##############################################################################


def input_features_check():
    '''
    This function checks whether all the input columns are present in our new
    data. This ensures the prediction pipeline doesn't break because of change in
    columns in input data.

    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be
        ONE_HOT_ENCODED_FEATURES: List of all the features which need to be present
        in our input data.

    OUTPUT
        It writes the output in a log file based on whether all the columns are present
        or not.
        1. If all the input columns are present then it logs - 'All the models input are present'
        2. Else it logs 'Some of the models inputs are missing'

    SAMPLE USAGE
        input_col_check()
    '''
    # read the input data
    conn = sqlite3.connect(DB_PATH+DB_FILE_NAME)
    df_inf = pd.read_sql('select * from features_inference', conn)

    # check if all columns are present
    check = set(df_inf.columns) == set(ONE_HOT_ENCODED_FEATURES)

    if check:
        print('All the models input are present')
    else:
        print('Some of the models inputs are missing')
   
