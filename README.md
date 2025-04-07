# Rockscraper Crawl Service

This service is a web crawling application that uses Docker for containerization.

## Environment Variables

The following environment variables are used in the application:

### Node Environment
- `NODE_ENV`: Specifies the Node.js environment (development/production)

### Database Configuration
- `POSTGRES_USER`: PostgreSQL database username
- `POSTGRES_PASSWORD`: PostgreSQL database password
- `POSTGRES_DB`: Name of the PostgreSQL database
- `POSTGRES_HOST`: Host address of the PostgreSQL server
- `POSTGRES_PORT`: Port number for PostgreSQL connection
- `DATABASE_URL`: Complete PostgreSQL connection URL

### API Configuration
- `API_TOKEN`: Authentication token for LLM API access

## Getting Started

To run the application:

1. Build the Docker containers:
```bash
docker compose build
```

2. Start the application:
```bash
docker compose up
```

The application will be available at the configured port (default: 5000).

## Development

For development purposes, you can use the provided `.env` file. Make sure to update the values according to your local setup if needed. 
