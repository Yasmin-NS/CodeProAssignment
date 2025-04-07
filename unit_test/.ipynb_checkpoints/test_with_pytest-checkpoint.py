##############################################################################
# Import the necessary modules
# #############################################################################
from utils import *
from constants import *

import warnings
warnings.filterwarnings("ignore")


###############################################################################
# Write test cases for load_data_into_db() function
# ##############################################################################

def test_load_data_into_db():
    """_summary_
    This function checks if the load_data_into_db function is working properly by
    comparing its output with test cases provided in the db in a table named
    'loaded_data_test_case'

    INPUTS
        DB_FILE_NAME : Name of the database file 'utils_output.db'
        DB_PATH : path where the db file should be present
        UNIT_TEST_DB_FILE_NAME: Name of the test database file 'unit_test_cases.db'

    SAMPLE USAGE
        output=test_get_data()

    """
    load_data_into_db()
    
    conn = sqlite3.connect(DB_PATH + DB_FILE_NAME)
    loaded_data = pd.read_sql('SELECT * FROM loaded_data', conn)
    conn.close()
    
    conn_ut = sqlite3.connect(DB_PATH + UNIT_TEST_DB_FILE_NAME)
    test_case_loaded_data = pd.read_sql('SELECT * FROM loaded_data_test_case', conn_ut)
    conn_ut.close()
    
    assert len(loaded_data.columns) == len(test_case_loaded_data.columns), "Column count does not match"
    

###############################################################################
# Write test cases for map_city_tier() function
# ##############################################################################
def test_map_city_tier():
    """_summary_
    This function checks if map_city_tier function is working properly by
    comparing its output with test cases provided in the db in a table named
    'city_tier_mapped_test_case'

    INPUTS
        DB_FILE_NAME : Name of the database file 'utils_output.db'
        DB_PATH : path where the db file should be present
        UNIT_TEST_DB_FILE_NAME: Name of the test database file 'unit_test_cases.db'

    SAMPLE USAGE
        output=test_map_city_tier()

    """
    map_city_tier()
    conn = sqlite3.connect(DB_PATH + DB_FILE_NAME)
    city_tier_map = pd.read_sql('SELECT * FROM city_tier_mapped', conn)
    conn.close()
    
    conn_ut = sqlite3.connect(DB_PATH + UNIT_TEST_DB_FILE_NAME)
    test_case_city_tier = pd.read_sql('SELECT * FROM city_tier_mapped_test_case', conn_ut)
    conn_ut.close()
    
    assert len(city_tier_map.columns) == len(test_case_city_tier.columns), "Column count does not match"
    
    

###############################################################################
# Write test cases for map_categorical_vars() function
# ##############################################################################    
def test_map_categorical_vars():
    """_summary_
    This function checks if map_cat_vars function is working properly by
    comparing its output with test cases provided in the db in a table named
    'categorical_variables_mapped_test_case'

    INPUTS
        DB_FILE_NAME : Name of the database file 'utils_output.db'
        DB_PATH : path where the db file should be present
        UNIT_TEST_DB_FILE_NAME: Name of the test database file 'unit_test_cases.db'
    
    SAMPLE USAGE
        output=test_map_cat_vars()

    """    
    map_categorical_vars()
    
    conn = sqlite3.connect(DB_PATH + DB_FILE_NAME)
    cat_var_map = pd.read_sql('SELECT * FROM categorical_variables_mapped', conn)
    conn.close()
    
    conn_ut = sqlite3.connect(DB_PATH + UNIT_TEST_DB_FILE_NAME)
    test_case_cat_var = pd.read_sql('SELECT * FROM categorical_variables_mapped_test_case', conn_ut)
    conn_ut.close()
    assert len(cat_var_map.columns) == len(test_case_cat_var.columns), "Column count does not match"

###############################################################################
# Write test cases for interactions_mapping() function
# ##############################################################################    
def test_interactions_mapping():
    """_summary_
    This function checks if test_column_mapping function is working properly by
    comparing its output with test cases provided in the db in a table named
    'interactions_mapped_test_case'

    INPUTS
        DB_FILE_NAME : Name of the database file 'utils_output.db'
        DB_PATH : path where the db file should be present
        UNIT_TEST_DB_FILE_NAME: Name of the test database file 'unit_test_cases.db'

    SAMPLE USAGE
        output=test_column_mapping()

    """ 
    interactions_mapping()
    
    conn = sqlite3.connect(DB_PATH + DB_FILE_NAME)
    int_map = pd.read_sql('SELECT * FROM interactions_mapped', conn)
    conn.close()
    
    conn_ut = sqlite3.connect(DB_PATH + UNIT_TEST_DB_FILE_NAME)
    test_case_int_map = pd.read_sql('SELECT * FROM interactions_mapped_test_case', conn_ut)
    conn_ut.close()
    
    assert len(int_map.columns) == len(test_case_int_map.columns), "Column count does not match"
