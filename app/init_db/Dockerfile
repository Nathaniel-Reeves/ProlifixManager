FROM python:3.9-slim-buster


# Set working directory
WORKDIR /init_db

# Copy application files
COPY ./init_db /init_db


# Prepare dependancies for mariadb-connector
USER root

RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y apt-transport-https 
RUN apt-get update && apt-get install -y wget
RUN wget https://dlm.mariadb.com/3/MariaDB/mariadb_repo_setup
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup --mariadb-server-version="mariadb-10.11"
RUN apt-get update && apt-get install -y mariadb-client
RUN apt-get update && apt-get install -y python3-pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb3 \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "load_db.py"]

