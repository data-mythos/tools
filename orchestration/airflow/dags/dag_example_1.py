"""
Basic Airflow DAG Example

This DAG demonstrates the fundamental concepts of Apache Airflow, including:
    - Task creation and dependencies
    - Different types of operators (DummyOperator and PythonOperator)
    - Basic DAG configuration and scheduling
    - Error handling with retries
    - Proper logging practices

DAG Structure:
    start -> task1 -> task2 -> end

DAG Parameters:
    - Schedule: Daily
    - Start Date: Jan 1, 2025
    - Catchup: False (won't backfill)
    - Retries: 3 attempts with 5-minute delay
"""

from airflow import DAG
from airflow.operators.empty import EmptyOperator as DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging

# Get Airflow's logger
logger = logging.getLogger(__name__)

def my_python_task(**context):
    """
    Example Python callable function that will be executed by PythonOperator.
    
    This function demonstrates proper logging in Airflow tasks. In real-world scenarios,
    this could be replaced with actual business logic like:
        - Data processing
        - API calls
        - Database operations
        - File handling
    
    Args:
        **context: Task context dictionary containing runtime variables
    
    Returns:
        None: Logs execution messages and task information
    """
    # Get task instance from context
    task_instance = context['task_instance']
    task_id = task_instance.task_id
    dag_id = task_instance.dag_id
    execution_date = context['execution_date']

    # Log task start
    logger.info(f"Starting task {task_id} in DAG {dag_id}")
    logger.info(f"Execution date: {execution_date}")

    try:
        # Your task logic here
        logger.info(f"Executing main logic for task {task_id}")
        
        # Example of different log levels
        logger.debug("This is a debug message with detailed information")
        logger.info("Task is processing normally")
        logger.warning("This is a warning example")
        
        # Simulate task success
        logger.info(f"Task {task_id} completed successfully")
        
    except Exception as e:
        # Log any errors that occur
        logger.error(f"Error in task {task_id}: {str(e)}", exc_info=True)
        raise  # Re-raise the exception to mark task as failed

# Define the DAG and its configurations
with DAG(
        'example_dag',              
        description='An example DAG to demonstrate workflow',
        schedule_interval='@daily',  
        start_date=datetime(2025, 1, 1),
        catchup=False,              
        default_args={
            'owner': 'airflow',     
            'retries': 3,           
            'retry_delay': timedelta(minutes=5),
        }
) as dag:
    
    logger.info("Initializing DAG 'example_dag'")
    
    # Start task: marks the beginning of the workflow
    start = DummyOperator(
        task_id='start',
        dag=dag,
    )
    logger.debug("Created 'start' task")
    
    # Task 1: First Python task
    task1 = PythonOperator(
        task_id='task_1',
        python_callable=my_python_task,
        provide_context=True,  # Provides runtime context to the callable
        dag=dag,
    )
    logger.debug("Created 'task_1'")
    
    # Task 2: Second Python task
    task2 = PythonOperator(
        task_id='task_2',
        python_callable=my_python_task,
        provide_context=True,
        dag=dag,
    )
    logger.debug("Created 'task_2'")
    
    # End task: marks the completion of the workflow
    end = DummyOperator(
        task_id='end',
        dag=dag,
    )
    logger.debug("Created 'end' task")

    # Define task dependencies
    start >> task1 >> task2 >> end
    logger.info("Task dependencies set: start >> task1 >> task2 >> end")

# Log DAG creation completion
logger.info("DAG 'example_dag' has been fully initialized")
