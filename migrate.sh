#!/bin/bash

# Check if the migration directory exists
 if [ ! -d /rockscraper-crawl-service/config/database_migrations_psql ]; then
   echo "Initializing migrations..."
   flask db init
 fi

echo "Running migrations..."
flask db stamp head
flask db migrate
flask db upgrade

echo "Starting Gunicorn..."
gunicorn --workers 1 --timeout 600 -b 0.0.0.0:5000 --reload crawl:app -k gevent
