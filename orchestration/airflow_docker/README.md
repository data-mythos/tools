# Setting Up Apache Airflow in Docker: A Complete Guide

#### Step-by-Step Explanation
1.**Version**:
* The version used in this configuration is version: '3', which specifies the version of Docker Compose.
* Version 3 is compatible with a wide range of Docker features, and it is a standard version used for modern setups.

2. **PostgreSQL Service**:

    The PostgreSQL service is essential for storing Airflow’s metadata. The service uses the postgres:13 Docker image and sets the following environment variables:

    
    **POSTGRES_USER**: Defines the username for connecting to PostgreSQL (e.g., airflow).

    **POSTGRES_PASSWORD**: The password associated with the user (airflow).

    **POSTGRES_DB**: The name of the database that will be created (e.g., airflow).

Additionally, the data is persisted using a volume (postgres_data) to ensure that the PostgreSQL data is not lost when the container is restarted or removed. 

The PostgreSQL container is connected to the airflow_network network to enable communication with other services.

3. **Redis Service**:

* The Redis service acts as the message broker for the CeleryExecutor in Airflow. 

* It is used to queue tasks that need to be processed by worker nodes. 

The Redis service uses the redis:latest Docker image and is connected to the airflow_network to facilitate communication with other services, such as the webserver and scheduler.

4. **Airflow Webserver Service**

The Airflow Webserver provides the user interface for interacting with Airflow. This service uses a custom Docker image (my_airflow_image), which includes additional libraries like Pandas and Dask.

Some key environment variables for the Airflow Webserver:

    **AIRFLOW__CORE__EXECUTOR**=CeleryExecutor: Specifies the executor to be used (CeleryExecutor).

    **AIRFLOW__CORE__SQL_ALCHEMY_CONN**: Defines the connection string for PostgreSQL.

    **AIRFLOW__WEBSERVER__RBAC**=True: Enables Role-Based Access Control (RBAC) for user authentication and authorization.

    **AIRFLOW__API__AUTH_BACKENDS**: Specifies the authentication backend (basic authentication in this case).

The Webserver is exposed on port 8080, making it accessible via a browser.

5. **Airflow Scheduler Service**

* The Airflow Scheduler schedules the execution of tasks and is responsible for triggering the tasks defined in your DAGs.

* This service uses the same custom Docker image (my_airflow_image) and connects to PostgreSQL and Redis for storing metadata and handling task queuing. The scheduler uses the command airflow scheduler to run the scheduler process.

6. **Airflow Worker Service**

* The Airflow Worker is responsible for executing tasks.

* It runs using the CeleryExecutor and is connected to Redis to fetch tasks from the queue.

* The worker service also uses the custom image with Pandas and Dask.

* The worker is defined to run the command celery worker, which is the Celery command to start a worker process.

7. **Airflow Flower Service**

* Flower is a real-time web-based tool for monitoring Celery tasks.

* It shows the status of workers, tasks, and queues. 

* This service uses the apache/airflow:2.5.1 Docker image and is exposed on port 5555.

* Flower connects to Redis to monitor the Celery task queues.

8. **Networks and Volumes**

* The configuration defines a custom network called airflow_network to enable communication between all the services.

* This custom network uses the bridge driver, which is the default networking driver for Docker containers.

* The postgres_data volume is defined to persist PostgreSQL data. This ensures that data stored in the database is not lost when the PostgreSQL container is stopped or removed.


```
# 1. Create Airflow admin user
# Login to docker container
docker-compose exec airflow-webserver bash

# Command to create admin user with password
airflow users  create --role Admin --username <"username"> --email <"email"> --firstname <"fname"> --lastname <"lname"> --password <"password">


# Airflow logs on Webserver
# Code to generate the secret key
import secrets
print(secrets.token_urlsafe(32))

# Command to build AIRFLOW__WEBSERVER__SECRET_KEY
# Purpose of AIRFLOW__WEBSERVER__SECRET_KEY:
# <b>Session Security:</b> Airflow uses sessions for storing user-related data in the web interface. 
# The SECRET_KEY is used to sign the session data, ensuring that no one can tamper with it.
# <b>Web Authentication:</b> If you enable web authentication, this key is used for securely signing the authentication tokens.
# <b>Preventing Cross-Site Request Forgery (CSRF):</b> The SECRET_KEY is also involved in preventing CSRF attacks by signing forms and requests.


# Build docker image
docker build -t my_airflow_image . 

# Run docker compose
docker-compose up --build -d
```