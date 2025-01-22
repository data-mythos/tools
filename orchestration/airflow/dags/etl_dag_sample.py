"""
Simple ETL DAG Example

This DAG demonstrates the basic structure of an Airflow DAG with two sequential tasks.
It serves as a template for creating more complex ETL workflows.

DAG Parameters:
    - Schedule: Daily
    - Start Date: Jan 19, 2025
    - Catchup: False (only run for current date)
"""

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import logging

# Get Airflow's logger
logger = logging.getLogger(__name__)

def greet_user(**context):
    """
    A simple Python callable that demonstrates logging in Airflow tasks.
    
    Args:
        **context: Task context containing runtime variables
    
    Returns:
        None: Logs greeting message and task information
    """
    # Get task instance from context
    task_instance = context['task_instance']
    task_id = task_instance.task_id
    execution_date = context['execution_date']

    try:
        logger.info(f"Starting task {task_id}")
        logger.info(f"Execution date: {execution_date}")
        
        # Task logic
        message = "Hello, Airflow!"
        logger.info(f"Generated message: {message}")
        
        # Log successful completion
        logger.info(f"Task {task_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Error in task {task_id}: {str(e)}", exc_info=True)
        raise

logger.info("Initializing ETL Sample DAG")

# Define default parameters for the DAG
default_args = {
    'owner': 'airflow',              # Owner of the DAG
    'start_date': datetime(2025, 1, 19),  # Date when DAG should start
    # Additional parameters you might want to add:
    # 'retries': 1,                  # Number of retries if task fails
    # 'retry_delay': timedelta(minutes=5),  # Delay between retries
    # 'email': ['your-email@domain.com'],  # Email for notifications
    # 'email_on_failure': False,     # Send email on task failure
}

# Initialize the DAG
dag = DAG(
    'simple_dag',                    # Unique identifier for the DAG
    default_args=default_args,       # Default arguments defined above
    schedule_interval='@daily',      # Run frequency
    # Additional parameters:
    # catchup=False,                 # Don't backfill missing runs
    # tags=['example', 'tutorial'],  # Tags for organizing DAGs
)

logger.debug("Created DAG object with default parameters")

# Define the first task
task1 = PythonOperator(
    task_id='greet_task',           # Unique identifier for the task
    python_callable=greet_user,      # Function to execute
    provide_context=True,
    dag=dag,                        # Associated DAG
)
logger.debug("Created task1: greet_task")

# Define the second task
task2 = PythonOperator(
    task_id='another_task',         # Unique identifier for the task
    python_callable=greet_user,      # Function to execute
    provide_context=True,
    dag=dag,                        # Associated DAG
)
logger.debug("Created task2: another_task")

# Set task dependencies: task1 must complete before task2 starts
task1 >> task2
logger.info("Task dependencies set: task1 >> task2")

logger.info("ETL Sample DAG initialization complete")

