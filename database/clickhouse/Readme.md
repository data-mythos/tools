# ClickHouse Database Setup

This directory contains the necessary configuration files and scripts to set up a ClickHouse database using Docker.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)
- At least 4GB of RAM available
- Ports 8123, 9000, and 9009 available on your host machine

## Directory Structure

```
clickhouse/
├── config/              # ClickHouse configuration files
│   ├── config.xml      # Main server configuration
│   └── users.xml       # User management and access control
├── init/               # Database initialization scripts
│   └── 01-init.sql     # Initial database and table creation
├── docker/             # Docker-related files
│   ├── Dockerfile      # Custom ClickHouse image definition
│   └── docker-compose.yml # Container orchestration
├── .env                # Environment variables
└── README.md           # Documentation
```

## Step-by-Step Setup Guide

### 1. Clone the Repository

```
# Navigate to your desired directory
git clone <repository-url>
cd database/clickhouse
```

### 2. Configure Environment Variables

Create a `.env` file if it doesn't exist:

```
cp .env.example .env
```

Edit the `.env` file with your preferred settings:

```
CLICKHOUSE_DB=social_media
CLICKHOUSE_USER=admin
CLICKHOUSE_PASSWORD=adminpassword
CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT=1
```

### 3. Understanding the Docker Configuration

#### Docker Compose File (`docker/docker-compose.yml`)

- **Version**: Specifies the version of the Docker Compose file format.
- **Services**: Defines the containers to be run.
  - **clickhouse**: The main ClickHouse server.
    - **image**: Specifies the Docker image to use.
    - **container_name**: The name of the container.
    - **environment**: Environment variables for configuring ClickHouse.
    - **ports**: Maps container ports to host ports.
    - **volumes**: Mounts directories for persistent storage and initialization scripts.
    - **networks**: Defines the network for container communication.
    - **restart**: Ensures the container restarts automatically on failure.
  - **tabix**: A web UI for ClickHouse.
    - **depends_on**: Ensures ClickHouse starts before the UI.
    - **environment**: Configures the UI to connect to ClickHouse.

#### Example Docker Compose File

```
version: '3.8'

services:
  clickhouse:
    image: clickhouse/clickhouse-server:latest
    container_name: clickhouse-db
    environment:
      - CLICKHOUSE_DB=social_media
      - CLICKHOUSE_USER=admin
      - CLICKHOUSE_PASSWORD=adminpassword
      - CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT=1
    ports:
      - "9000:9000"
      - "8123:8123"
      - "9009:9009"
    volumes:
      - clickhouse_data:/var/lib/clickhouse
      - ../init:/docker-entrypoint-initdb.d
    networks:
      - clickhouse-net
    restart: always

  tabix:
    image: spoonest/clickhouse-tabix-web-client
    container_name: clickhouse-ui
    ports:
      - "8080:80"
    depends_on:
      - clickhouse
    environment:
      - CH_NAME=social_media
      - CH_HOST=clickhouse
      - CH_PORT=8123
      - CH_USER=admin
      - CH_PASSWORD=adminpassword
    networks:
      - clickhouse-net
    restart: always

networks:
  clickhouse-net:
    driver: bridge

volumes:
  clickhouse_data:
```

### 4. Start the ClickHouse Server

Run the following commands to start the ClickHouse server and the UI:

```
cd docker
docker-compose up -d
```

### 5. Access the ClickHouse UI

Open your web browser and navigate to:

```
http://localhost:8080
```

- **Login Credentials**:
  - **Username**: admin
  - **Password**: adminpassword

### 6. Create Required Tables Using the UI

1. After logging in, navigate to the SQL query editor.
2. Run the following SQL commands to create the necessary tables:

```
-- Create users table
CREATE TABLE IF NOT EXISTS users
(
    user_id UUID DEFAULT generateUUIDv4(),
    username String,
    email String,
    full_name String,
    created_at DateTime DEFAULT now(),
    last_login DateTime DEFAULT now(),
    is_active UInt8 DEFAULT 1
) ENGINE = MergeTree()
ORDER BY (user_id);

-- Create posts table
CREATE TABLE IF NOT EXISTS posts
(
    post_id UUID DEFAULT generateUUIDv4(),
    user_id UUID,
    content String,
    created_at DateTime DEFAULT now(),
    likes UInt32 DEFAULT 0,
    shares UInt32 DEFAULT 0,
    is_deleted UInt8 DEFAULT 0
) ENGINE = MergeTree()
ORDER BY (created_at, user_id);

-- Create comments table
CREATE TABLE IF NOT EXISTS comments
(
    comment_id UUID DEFAULT generateUUIDv4(),
    post_id UUID,
    user_id UUID,
    content String,
    created_at DateTime DEFAULT now(),
    likes UInt32 DEFAULT 0,
    is_deleted UInt8 DEFAULT 0
) ENGINE = MergeTree()
ORDER BY (created_at, post_id);
```

### 7. Best Practices

- **Data Backup**: Regularly back up your ClickHouse data using the built-in backup features or by copying the data directory.
- **Monitoring**: Use monitoring tools to keep track of resource usage and query performance.
- **Resource Allocation**: Ensure that your Docker containers have sufficient resources (CPU, memory) allocated to handle your workload.
- **Security**: Use strong passwords for users and limit access to the ClickHouse server.

### 8. Monitoring Steps

1. **Check Container Status**:
   ```bash
   docker-compose ps
   ```

2. **View Logs**:
   ```bash
   docker-compose logs -f clickhouse
   ```

3. **Monitor Resource Usage**:
   ```bash
   docker stats
   ```

4. **Query Performance**:
   Use the ClickHouse system tables to monitor query performance:
   ```sql
   SELECT *
   FROM system.query_log
   ORDER BY event_time DESC
   LIMIT 10;
   ```

## Conclusion

You now have a fully functional ClickHouse database running in Docker with a web UI for management. You can create tables, insert data, and monitor performance using the provided tools. Follow best practices for security and resource management to ensure optimal performance.

## Additional Resources

- [ClickHouse Documentation](https://clickhouse.com/docs)
- [Docker Hub - ClickHouse](https://hub.docker.com/r/clickhouse/clickhouse-server)
- [ClickHouse GitHub](https://github.com/ClickHouse/ClickHouse)





