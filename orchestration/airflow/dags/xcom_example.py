"""
XCom Example DAG

This DAG demonstrates the usage of XCom (Cross-Communication) in Airflow,
which allows tasks to exchange small amounts of data.

Features demonstrated:
    - XCom push: Storing data for other tasks
    - XCom pull: Retrieving data from previous tasks
    - Task context usage
    - Manual triggering (no schedule)

DAG Parameters:
    - Schedule: None (manual triggers only)
    - Start Date: Jan 1, 2025
    - Catchup: False
"""

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import random
import logging

# Get Airflow's logger
logger = logging.getLogger(__name__)

# Function to push a value to XCom
def push_value_to_xcom(**context):
    """
    Generates a random number and pushes it to XCom.
    
    Args:
        **context: Task context containing runtime variables
    """
    task_instance = context['task_instance']
    task_id = task_instance.task_id
    
    try:
        logger.info(f"Starting task {task_id}")
        
        # Generate random value
        random_value = random.randint(1, 100)
        logger.debug(f"Generated random value: {random_value}")
        
        # Push to XCom
        task_instance.xcom_push(key='random_number', value=random_value)
        logger.info(f"Successfully pushed value {random_value} to XCom")
        
    except Exception as e:
        logger.error(f"Error in task {task_id}: {str(e)}", exc_info=True)
        raise

# Function to pull a value from XCom and use it
def pull_value_from_xcom_and_process(**context):
    """
    Retrieves and processes the random number from XCom.
    
    Args:
        **context: Task context containing runtime variables
    """
    task_instance = context['task_instance']
    task_id = task_instance.task_id
    
    try:
        logger.info(f"Starting task {task_id}")
        
        # Pull value from XCom
        random_value = task_instance.xcom_pull(task_ids='task_1', key='random_number')
        logger.debug(f"Retrieved value from XCom: {random_value}")
        
        if random_value is not None:
            processed_value = random_value * 2
            logger.info(f"Processed value (doubled): {processed_value}")
        else:
            logger.warning("No value found in XCom")
            
    except Exception as e:
        logger.error(f"Error in task {task_id}: {str(e)}", exc_info=True)
        raise

logger.info("Initializing XCom Example DAG")

# Define the DAG
with DAG(
    'xcom_example',
    description='An example DAG to demonstrate XCom usage',
    schedule_interval=None,  # Set to None to trigger manually
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:

    logger.debug("Creating DAG tasks")
    
    # Task 1: Push value to XCom
    task_1 = PythonOperator(
        task_id='task_1',
        python_callable=push_value_to_xcom,
        provide_context=True  # Pass context (like task instance) to the function
    )
    logger.debug("Created task_1: push_value_to_xcom")

    # Task 2: Pull value from XCom and process it
    task_2 = PythonOperator(
        task_id='task_2',
        python_callable=pull_value_from_xcom_and_process,
        provide_context=True  # Pass context to the function
    )
    logger.debug("Created task_2: pull_value_from_xcom_and_process")

    # Set the task dependencies
    task_1 >> task_2
    logger.info("Task dependencies set: task_1 >> task_2")

logger.info("XCom Example DAG initialization complete")
