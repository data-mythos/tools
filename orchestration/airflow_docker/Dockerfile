FROM apache/airflow:2.7.2

# Install additional packages
USER airflow
RUN pip install --no-cache-dir \
    dask[complete] \
    distributed \
    pandas \
