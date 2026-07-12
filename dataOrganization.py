import pandas as pd
import numpy as np
import xgboost as xgb
from lifelines import WeibullAFTFitter
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import sqlite3

excel_file = 'online_retail_II.xlsx'
df = pd.read_excel(excel_file)


#create an in-memory SQL database (would be Snowflake, BigQuery, or similar)
conn = sqlite3.connect(':memory:')

#transfer the DataFrame to the SQL database as a relational table
df.to_sql('retail_data', conn, index=False, if_exists='replace')

#Filter data through CTEs and window functions
sql_query = """
WITH cleaned_data AS (
    -- filter out cancellations, convert strings to timestamps, clean nulls
    SELECT
        CAST

"""