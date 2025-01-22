# Use official Apache Airflow image as base
# Version 2.7.2 is stable and includes Python 3.9
FROM apache/airflow:2.7.2

# Switch to airflow user for security best practices
# Apache Airflow runs as non-root user 'airflow' by default
USER airflow

# Install additional Python packages
# --no-cache-dir reduces image size by not caching pip packages
RUN pip install --no-cache-dir \
    # Dask[complete] includes all Dask components for distributed computing
    dask[complete] \
    # Distributed is required for Dask's distributed scheduler
    distributed \
    # Pandas for data manipulation and analysis
    pandas \
    # Add any additional packages below
    # package-name==version

# Note: If you need system packages, add them before USER airflow:
# USER root
# RUN apt-get update && apt-get install -y \
#     package-name \
#     && rm -rf /var/lib/apt/lists/*
# USER airflow
