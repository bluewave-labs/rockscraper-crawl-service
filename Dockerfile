# Base image
FROM mcr.microsoft.com/playwright/python:v1.51.0-noble

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=crawl.py

# Set the working directory
WORKDIR /rockscraper-crawl-service

# Install Python dependencies
COPY /requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

COPY migrate.sh /migrate.sh
RUN chmod +x /migrate.sh

# Switch to non-root user for security
USER pwuser

CMD ["/migrate.sh"]
