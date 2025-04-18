FROM ubuntu:22.04

# Install Python and other dependencies
RUN apt-get update && \
    apt-get install -y \
    python3.12 \
    python3.12-dev \
    python3-pip \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.12 as default
RUN ln -sf /usr/bin/python3.12 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.12 /usr/bin/python

# Install Playwright and its dependencies
RUN pip3 install playwright==1.51.0

# Install only Chromium browser
RUN playwright install chromium

# Set working directory
WORKDIR /app

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
