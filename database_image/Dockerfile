FROM python:3.9-slim-buster

# Install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb3 \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /database_image

# Copy application files
COPY . /database_image

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Set entrypoint script
ENTRYPOINT ["/database_image/entrypoint.sh"]