FROM python:3.9-slim-buster


# Set working directory
WORKDIR /main

# Copy application files
COPY ./api/main /main
COPY ./client/public /main/public
COPY ./.env ./.env

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

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:create_app()"]
