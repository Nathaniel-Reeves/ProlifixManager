#!/bin/bash

# Load environment variables
if [ -f .env ]; then
    source .env
else
    echo "Error: .env file not found"
    exit 1
fi

# Check if required variables are set
if [ -z "$DB_BACKUP_USER" ] || [ -z "$DB_BACKUP_PASSWORD" ] || [ -z "$BACKUP_ENCRYPTION_KEY"]; then
    echo "Error: DB_BACKUP_USER or DB_BACKUP_PASSWORD or BACKUP_ENCRYPTION_KEY is not set in .env file"
    exit 1
fi

# Create backup directory with timestamp
timestamp=$(date '+%Y-%m-%d-%H-%M-%S')
mkdir -p server_backup_$timestamp

# Create a mariadb_backup_user_creds.cnf
echo "[backup]" > mariadb_backup_user_creds.cnf
echo "user=$DB_BACKUP_USER" >> mariadb_backup_user_creds.cnf
echo "password=$DB_BACKUP_PASSWORD" >> mariadb_backup_user_creds.cnf

# Generate Backup SQL file
docker compose exec -T mariadb sh -c 'mariadb-dump --defaults-file=./mariadb_backup_user_creds.cnf --lock-tables --all-databases > /docker-entrypoint-initdb.d/mariadb_backup.sql'

# Move mariadb_backup.sql to new server_backup_ directory
mv ./db/mariadb_backup.sql server_backup_$timestamp/mariadb_backup.sql

# Copy the /var/samba_drive_share directory and place it in the server_backup_ directory
cp -r /var/samba_drive_share server_backup_$timestamp/samba_drive_share_backup

# Compress and encrypt the server_backup_ directory and remove the original server_backup_ directory
tar -czf server_backup_$timestamp.tar.gz server_backup_$timestamp | gpg -c --passphrase $BACKUP_ENCRYPTION_KEY > server_backup_$timestamp.tar.gz.gpg
rm -rf server_backup_$timestamp

# Send the encrypted backup file to the backup server

