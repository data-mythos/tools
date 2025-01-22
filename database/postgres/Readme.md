# PostgreSQL Database Setup

This directory contains the necessary configuration files and scripts to set up a PostgreSQL database using Docker.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)
- At least 2GB of RAM available
- Ports 5432 available on your host machine

## Directory Structure

```
postgres/
├── init/               # Database initialization scripts
│   └── init.sql       # Initial database and table creation
├── docker/             # Docker-related files
│   └── docker-compose.yml # Container orchestration
├── .env                # Environment variables
└── README.md           # Documentation
```

## Step-by-Step Setup Guide

### 1. Clone the Repository

```
# Navigate to your desired directory
git clone <repository-url>
cd database/postgres
```

### 2. Configure Environment Variables

Create a `.env` file if it doesn't exist:

```
cp .env.example .env
```

Edit the `.env` file with your preferred settings:

```
POSTGRES_DB=mydatabase
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
```

### 3. Understanding the Docker Configuration

#### Docker Compose File (`docker/docker-compose.yml`)

- **Version**: Specifies the version of the Docker Compose file format.
- **Services**: Defines the containers to be run.
  - **postgres**: The main PostgreSQL server.
    - **image**: Specifies the Docker image to use.
    - **container_name**: The name of the container.
    - **environment**: Environment variables for configuring PostgreSQL.
    - **ports**: Maps container ports to host ports.
    - **volumes**: Mounts directories for persistent storage and initialization scripts.
    - **restart**: Ensures the container restarts automatically on failure.

#### Example Docker Compose File

```
version: '3.8'

services:
  postgres:
    image: postgres:latest
    container_name: postgres-db
    environment:
      - POSTGRES_DB=mydatabase
      - POSTGRES_USER=myuser
      - POSTGRES_PASSWORD=mypassword
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ../init:/docker-entrypoint-initdb.d
    restart: always

volumes:
  postgres_data:
```

### 4. Start the PostgreSQL Server

Run the following commands to start the PostgreSQL server:

```
cd docker
docker-compose up -d
```

### 5. Access the PostgreSQL Database

You can access the PostgreSQL database using a PostgreSQL client or through the command line:

```
# Using psql command line
docker exec -it postgres-db psql -U myuser -d mydatabase
```

### 6. Initialize Data Using SQL Scripts

1. Place your SQL initialization scripts in the `init/` directory.
2. The scripts will be executed automatically when the container starts.

Example `init.sql` file:

```
-- Create a sample table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO users (username, email) VALUES
('john_doe', 'john@example.com'),
('jane_smith', 'jane@example.com');
```

### 7. Best Practices

- **Data Backup**: Regularly back up your PostgreSQL data using the built-in backup features or by copying the data directory.
- **Monitoring**: Use monitoring tools to keep track of resource usage and query performance.
- **Resource Allocation**: Ensure that your Docker containers have sufficient resources (CPU, memory) allocated to handle your workload.
- **Security**: Use strong passwords for users and limit access to the PostgreSQL server.

### 8. Monitoring Steps

1. **Check Container Status**:
   ```bash
   docker-compose ps
   ```

2. **View Logs**:
   ```bash
   docker-compose logs -f postgres
   ```

3. **Monitor Resource Usage**:
   ```bash
   docker stats
   ```

4. **Query Performance**:
   Use the PostgreSQL system views to monitor query performance:
   ```sql
   SELECT *
   FROM pg_stat_activity;
   ```

## Conclusion

You now have a fully functional PostgreSQL database running in Docker. You can create tables, insert data, and monitor performance using the provided tools. Follow best practices for security and resource management to ensure optimal performance.

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Hub - PostgreSQL](https://hub.docker.com/_/postgres)
- [PostgreSQL GitHub](https://github.com/postgres/postgres)
