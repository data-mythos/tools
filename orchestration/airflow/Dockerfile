# Use official Apache Airflow image as base
FROM apache/airflow:2.7.3-python3.9

# Switch to root user to install additional packages
USER root

# Install additional Python packages
RUN pip install --no-cache-dir \
    clickhouse-sqlalchemy \
    dask[complete] \
    distributed \
    pandas

# Switch back to airflow user for security best practices
USER airflow