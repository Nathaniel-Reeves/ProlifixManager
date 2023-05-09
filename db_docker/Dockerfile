FROM python:3.9-slim-buster

# Prepare dependancies for mariadb-connector
USER root

RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y apt-transport-https 
RUN apt-get update && apt-get install -y wget
RUN wget https://dlm.mariadb.com/3/MariaDB/mariadb_repo_setup
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup --os-type=debian --os-version=11 --arch=x86_64
RUN apt-get update && apt-get install -y mariadb-client
RUN apt-get update && apt-get install -y python3-pip
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

