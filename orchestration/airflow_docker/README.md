# Setting Up Apache Airflow in Docker: A Complete Guide

## Project Structure
```
airflow_docker/
├── dags/                 # Store your DAG files
├── logs/                 # Airflow logs directory
├── plugins/              # Custom Airflow plugins
├── config/              # Configuration files
├── Dockerfile           # Custom Airflow image definition
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
└── docker-compose.yaml  # Docker services configuration
```

## Prerequisites
- Docker Engine (20.10.0 or later)
- Docker Compose (2.0.0 or later)
- Minimum 4GB RAM
- Git

## Setup Instructions

### 1. Initial Setup
```bash
# Create required directories
mkdir -p ./dags ./logs ./plugins ./config

# Copy environment file
cp .env.example .env

# Generate a secret key for Airflow webserver
python -c 'import secrets; print(secrets.token_urlsafe(32))'
# Add the generated key to .env file as AIRFLOW__WEBSERVER__SECRET_KEY
```

### 2. Build Custom Airflow Image
```bash
# Build the image
docker build -t my_airflow_image .
```

### 3. Start Airflow Services
```bash
# Start all services in detached mode
docker-compose up -d

# Check if all services are running
docker-compose ps
```

### 4. Create Admin User
For Linux:
```bash
# Create initial admin user
docker exec -it airflow-webserver airflow users create \
    --username <username> \
    --firstname <first_name> \
    --lastname <last_name> \
    --role Admin \
    --email <email> \
    --password <password>
```

For Windows (PowerShell/CMD):
```powershell
# Create initial admin user (single line)
docker exec -it airflow-webserver airflow users create --username <username> --firstname <first_name> --lastname <last_name> --role Admin --email <email> --password <password>
```

## Accessing Services
- **Airflow UI**: http://localhost:8080
  - Username: airflow
  - Password: airflow123
- **Flower** (Celery monitoring): http://localhost:5555

## Key Components

### 1. PostgreSQL (Metadata Database)
- Stores Airflow metadata
- Persists data using named volume
- Runs on default port 5432 (internal)

### 2. Redis (Message Broker)
- Handles task queue for CeleryExecutor
- Enables task distribution to workers
- Secured with password from .env

### 3. Airflow Components
- **Webserver**: UI interface (port 8080)
- **Scheduler**: Triggers task execution
- **Worker**: Executes the tasks
- **Flower**: Monitors Celery tasks (port 5555)

## Common Operations

### View Service Logs
```bash
# View logs for specific service
docker-compose logs -f airflow-webserver
```

### Scale Workers
```bash
# Scale to 3 workers
docker-compose up -d --scale airflow-worker=3
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

## Troubleshooting

### Common Issues
1. **Services fail to start**
   - Check logs: `docker-compose logs [service_name]`
   - Verify memory allocation
   - Ensure ports aren't in use

2. **Login issues**
   - If default login fails, create a new user using the commands above
   - Verify user exists: `docker exec -it airflow-webserver airflow users list`
   - Check webserver logs: `docker logs airflow-webserver`

3. **Permission issues**
   - For Linux users, set AIRFLOW_UID: `echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env`
   - For Windows users, set: `echo AIRFLOW_UID=50000 > .env`
   - Restart services after setting: `docker-compose down -v && docker-compose up -d`

## Security Notes
1. Change default passwords in .env
2. Generate unique secret key
3. Enable RBAC (already configured)
4. Regular updates and backups
5. Restrict network access in production

## Environment Variables
Key variables to set in `.env`:
```
POSTGRES_USER=airflow
POSTGRES_PASSWORD=secure_password
REDIS_PASSWORD=secure_password
AIRFLOW__WEBSERVER__SECRET_KEY=generated_key
```

## Maintenance

### Backup Database
```bash
docker-compose exec postgres pg_dump -U airflow airflow > backup.sql
```

### Update Airflow
1. Update version in Dockerfile
2. Rebuild: `docker-compose up -d --build`