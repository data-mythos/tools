from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator

# Sample data for the first DataFrame
data_1 = {
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie']
}

# Sample data for the second DataFrame
data_2 = {
    'id': [1, 2, 4],
    'age': [25, 30, 28]
}


# Function to perform the join operation
def join_dataframes():
    # Create DataFrames from the sample data
    df1 = pd.DataFrame(data_1)
    df2 = pd.DataFrame(data_2)

    # Perform an inner join on the 'id' column
    result_df = pd.merge(df1, df2, on='id', how='inner')

    # Print the result to the Airflow logs (for visibility)
    print("Joined DataFrame:")
    print(result_df)


# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
        'pandas_dataframe_join',
        default_args=default_args,
        description='A simple DAG to join two Pandas DataFrames',
        schedule_interval=None,  # Run on demand
        start_date=datetime(2025, 1, 6),
        catchup=False
) as dag:
    # Define the task to run the join operation
    join_task = PythonOperator(
        task_id='join_dataframes_task',
        python_callable=join_dataframes
    )

    # Set task dependencies (if you have multiple tasks, you can chain them)
    join_task
