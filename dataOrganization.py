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

'''
columns = df.columns.tolist()
print("Columns in the dataset:", columns)
#Columns in the dataset: 
#['Invoice', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'Price', 'Customer ID', 'Country']
'''

#Filter data through CTEs and window functions
sql_query = """
WITH cleaned_data AS (
    -- filter out cancellations, convert strings to timestamps, clean nulls
    SELECT
        CAST([Customer ID] AS INT) AS customer_id
        CAST(Quantity AS INT) AS quantity
        CAST(Price AS FLOAT) AS price
        CAST(Quantity AS INT) * CAST(Price AS FLOAT) AS total_price
        Invoice AS invoice
        dateTime(InvoiceDate) AS invoice_date
    FROM retail_data
    WHERE [Customer ID] IS NOT NULL
        AND Invoice NOT LIKE 'C%'  -- filter out cancellations, start with 'C'
),

transaction_gaps AS (
    -- calculate the time gap between transactions for each customer
    SELECT
        customer_id,
        invoice_date,
        JULIANDAY(invoice_date) - JULIANDAY(LAG(invoice_date, 1) OVER(
        PARTITION BY customer_id 
        ORDER BY invoice_date
    )) AS transaction_time_gap
FROM cleaned_data
),






    
    
"""