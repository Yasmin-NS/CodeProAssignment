##############################################################################
# Import necessary modules and files
# #############################################################################


import pandas as pd
import os
import sqlite3
from sqlite3 import Error

from constants import *
from significant_categorical_level import *
from city_tier_mapping import city_tier_mapping
###############################################################################
# Define the function to build database
# ##############################################################################

def build_dbs():
    '''
    This function checks if the db file with specified name is present 
    in the /Assignment/01_data_pipeline/scripts folder. If it is not present it creates 
    the db file with the given name at the given path. 


    INPUTS
        DB_FILE_NAME : Name of the database file 'utils_output.db'
        DB_PATH : path where the db file should exist  


    OUTPUT
    The function returns the following under the given conditions:
        1. If the file exists at the specified path
                prints 'DB Already Exists' and returns 'DB Exists'

        2. If the db file is not present at the specified loction
                prints 'Creating Database' and creates the sqlite db 
                file at the specified path with the specified name and 
                once the db file is created prints 'New DB Created' and 
                returns 'DB created'


    SAMPLE USAGE
        build_dbs()
    '''
    if os.path.isfile(DB_PATH+DB_FILE_NAME):
        print("DB Already Exsist")
        return "DB Exsists"
    else:
        print("Creating Database")
        #create a database connection to a SQLite database
        connection = None
        try:
            connection = sqlite3.connect(DB_PATH+DB_FILE_NAME)
            print("New DB Created")
        except Error as e:
            print(e)
            return "Error"
        finally:
            if connection:
                connection.close()
                return "DB Created"

###############################################################################
# Define function to load the csv file to the database
# ##############################################################################

def load_data_into_db():
    '''
    Thie function loads the data present in data directory into the db
    which was created previously.
    It also replaces any null values present in 'toal_leads_dropped' and
    'referred_lead' columns with 0.


    INPUTS
        DB_FILE_NAME : Name of the database file
        DB_PATH : path where the db file should be
        DATA_DIRECTORY : path of the directory where 'leadscoring.csv' 
                        file is present
        

    OUTPUT
        Saves the processed dataframe in the db in a table named 'loaded_data'.
        If the table with the same name already exsists then the function 
        replaces it.


    SAMPLE USAGE
        load_data_into_db()
    '''
    connection = sqlite3.connect(DB_PATH+DB_FILE_NAME)
    
    df_lead_scoring = pd.read_csv(DATA_DIRECTORY+'leadscoring.csv',index_col=0)

    df_lead_scoring['total_leads_droppped'] = df_lead_scoring['total_leads_droppped'].fillna(0)
    df_lead_scoring['referred_lead'] = df_lead_scoring['referred_lead'].fillna(0)

    df_lead_scoring.to_sql(name='loaded_data', con=connection, if_exists='replace', index=False)

    connection.close()
    return "Writing to DataBase loaded_data Done or Data Already was in Table. Check Logs."


###############################################################################
# Define function to map cities to their respective tiers
# ##############################################################################

    
def map_city_tier():
    '''
    This function maps all the cities to their respective tier as per the
    mappings provided in the city_tier_mapping.py file. If a
    particular city's tier isn't mapped(present) in the city_tier_mapping.py 
    file then the function maps that particular city to 3.0 which represents
    tier-3.


    INPUTS
        DB_FILE_NAME : Name of the database file
        DB_PATH : path where the db file should be
        city_tier_mapping : a dictionary that maps the cities to their tier

    
    OUTPUT
        Saves the processed dataframe in the db in a table named
        'city_tier_mapped'. If the table with the same name already 
        exsists then the function replaces it.

    
    SAMPLE USAGE
        map_city_tier()

    '''
    connection = sqlite3.connect(DB_PATH+DB_FILE_NAME)
    
    df_lead_scoring = pd.read_sql('select * from loaded_data', connection)

    df_lead_scoring["city_tier"] = df_lead_scoring["city_mapped"].map(city_tier_mapping)
    df_lead_scoring["city_tier"] = df_lead_scoring["city_tier"].fillna(3.0)
    df_lead_scoring = df_lead_scoring.drop(['city_mapped'], axis=1)

    df_lead_scoring.to_sql(name='city_tier_mapped', con=connection, if_exists='replace', index=False)

    connection.close()
    return "Writing to DataBase city_tier_mapped Done or Data Already was in Table. Check Logs."
    

###############################################################################
# Define function to map insignificant categorial variables to "others"
# ##############################################################################


def map_categorical_vars():
    '''
    This function maps all the insignificant variables present in 'first_platform_c'
    'first_utm_medium_c' and 'first_utm_source_c'. The list of significant variables
    should be stored in a python file in the 'significant_categorical_level.py' 
    so that it can be imported as a variable in utils file.
    

    INPUTS
        DB_FILE_NAME : Name of the database file
        DB_PATH : path where the db file should be present
        list_platform : list of all the significant platform.
        list_medium : list of all the significat medium
        list_source : list of all rhe significant source

        **NOTE : list_platform, list_medium & list_source are all constants and
                 must be stored in 'significant_categorical_level.py'
                 file. The significant levels are calculated by taking top 90
                 percentils of all the levels. For more information refer
                 'data_cleaning.ipynb' notebook.
  

    OUTPUT
        Saves the processed dataframe in the db in a table named
        'categorical_variables_mapped'. If the table with the same name already 
        exsists then the function replaces it.

    
    SAMPLE USAGE
        map_categorical_vars()
    '''
    connection = sqlite3.connect(DB_PATH+DB_FILE_NAME)

    df_lead_scoring = pd.read_sql('select * from city_tier_mapped', connection)

    new_df = df_lead_scoring[~df_lead_scoring['first_platform_c'].isin(list_platform)]
    # replace the value of these levels to others
    new_df['first_platform_c'] = "others"
    # get rows for levels which are present in list_platform
    old_df = df_lead_scoring[df_lead_scoring['first_platform_c'].isin(list_platform)]  
    # concatenate new_df and old_df to get the final dataframe
    df = pd.concat([new_df, old_df])

    # get rows for levels which are not present in list_medium
    new_df = df[~df['first_utm_medium_c'].isin(list_medium)]
    # replace the value of these levels to others
    new_df['first_utm_medium_c'] = "others"
    # get rows for levels which are present in list_medium
    old_df = df[df['first_utm_medium_c'].isin(list_medium)]
    # concatenate new_df and old_df to get the final dataframe
    df = pd.concat([new_df, old_df])

    # get rows for levels which are not present in list_source
    new_df = df[~df['first_utm_source_c'].isin(list_source)]
    # replace the value of these levels to others
    new_df['first_utm_source_c'] = "others"
    # get rows for levels which are present in list_source
    old_df = df[df['first_utm_source_c'].isin(list_source)]
    # concatenate new_df and old_df to get the final dataframe
    df = pd.concat([new_df, old_df])

    df = df.drop_duplicates()

    df.to_sql(name='categorical_variables_mapped', con=connection, if_exists='replace', index=False)
    connection.close()
    return "Writing to DataBase categorical_variables_mapped Done Check Logs."


##############################################################################
# Define function that maps interaction columns into 4 types of interactions
# #############################################################################
def interactions_mapping():
    '''
    This function maps the interaction columns into 4 unique interaction columns
    These mappings are present in 'interaction_mapping.csv' file. 


    INPUTS
        DB_FILE_NAME: Name of the database file
        DB_PATH : path where the db file should be present
        INTERACTION_MAPPING : path to the csv file containing interaction's
                                   mappings
        INDEX_COLUMNS_TRAINING : list of columns to be used as index while pivoting and
                                 unpivoting during training
        INDEX_COLUMNS_INFERENCE: list of columns to be used as index while pivoting and
                                 unpivoting during inference
        NOT_FEATURES: Features which have less significance and needs to be dropped
                                 
        NOTE : Since while inference we will not have 'app_complete_flag' which is
        our label, we will have to exculde it from our features list. It is recommended 
        that you use an if loop and check if 'app_complete_flag' is present in 
        'categorical_variables_mapped' table and if it is present pass a list with 
        'app_complete_flag' column, or else pass a list without 'app_complete_flag'
        column.

    
    OUTPUT
        Saves the processed dataframe in the db in a table named 
        'interactions_mapped'. If the table with the same name already exsists then 
        the function replaces it.
        
        It also drops all the features that are not requried for training model and 
        writes it in a table named 'model_input'

    
    SAMPLE USAGE
        interactions_mapping()
    '''
    connection = sqlite3.connect(DB_PATH+DB_FILE_NAME)

    df = pd.read_sql('select * from categorical_variables_mapped', connection)
    
    if 'app_complete_flag' in df.columns:
        index_variable = INDEX_COLUMNS_TRAINING
    else:
        index_variable = INDEX_COLUMNS_INFERENCE
        
    df_event_mapping = pd.read_csv(INTERACTION_MAPPING, index_col=[0])
    df_unpivot = pd.melt(df, id_vars=index_variable, var_name='interaction_type', value_name='interaction_value')
    df_unpivot['interaction_value'] = df_unpivot['interaction_value'].fillna(0)
    df = pd.merge(df_unpivot, df_event_mapping,on='interaction_type', how='left')
    df = df.drop(['interaction_type'], axis=1)
    df_pivot = df.pivot_table(values='interaction_value', index=index_variable, columns='interaction_mapping', aggfunc='sum')
    df_pivot = df_pivot.reset_index()
    
    df_pivot.to_sql(name='interactions_mapped', con=connection, if_exists='replace', index=False)
    
    df_model_input = df_pivot.drop(NOT_FEATURES, axis=1)
    df_model_input.to_sql(name='model_input', con=connection, if_exists='replace', index=False)
    
    connection.close()
    return "Writing to DataBase- interactions_mapped Done . Check Logs."
    
   
