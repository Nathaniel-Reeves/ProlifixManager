#!/bin/bash
echo "Configuring MariaDB..."

# Load environment variables
if [ -f .env ]; then
    source .env
else
    echo "Error: .env file not found"
    exit 1
fi

# Check if required variables are set
if [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ] || [ -z "$MARIADB_ROOT_PASSWORD" ]; then
    echo "Error: DB_USER or DB_PASSWORD or MARIADB_ROOT_PASSWORD is not set in .env file"
    exit 1
fi

apt-get update && apt-get install -y mariadb-client

# Grant root user remote access from any host
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host "$DB_HOST" -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '$MARIADB_ROOT_PASSWORD' WITH GRANT OPTION;"
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host "$DB_HOST" -e "FLUSH PRIVILEGES;"

echo "Remote access for root user from any host has been granted."

# Execute SQL commands to create the client user
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host "$DB_HOST" -e "CREATE USER '$DB_USER'@'%' IDENTIFIED BY '$DB_PASSWORD';"
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host "$DB_HOST" -e "GRANT ALL PRIVILEGES ON *.* TO '$DB_USER'@'%';"
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host "$DB_HOST" -e "FLUSH PRIVILEGES;"

echo "User $DB_USER has been created and granted all privileges."

# Execute SQL commands to create database backup user
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host "$DB_HOST" -e "CREATE USER '$DB_BACKUP_USER'@'%' IDENTIFIED BY '$DB_BACKUP_PASSWORD';"
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host "$DB_HOST" -e "GRANT SELECT, SHOW VIEW, TRIGGER, EVENT, RELOAD, LOCK TABLES ON *.* TO '$DB_BACKUP_USER'@'$DB_BACKUP_HOST';"
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host "$DB_HOST" -e "FLUSH PRIVILEGES;"

echo "User backup has been created and granted SELECT, SHOW VIEW, TRIGGER, EVENT, RELOAD, LOCK TABLES privileges."

# Set Time zone to UTC
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host "$DB_HOST" -e "SET GLOBAL time_zone = '+00:00'";

# Setup OQGraph engine for Mariadb
# apt update
# apt upgrade -y
# apt-get install mariadb-plugin-oqgraph
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host "$DB_HOST" -e "INSTALL SONAME 'ha_oqgraph';"
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host "$DB_HOST" -e "SHOW ENGINES;"

echo "OQGraph engine is installed."

# Do not execute sql files if database already exists (look in /var/lib for mysql directory)
if [ -d "/var/lib/mysql/Organizations" ]; then
    echo "Databases already exist. Skipping execution of SQL files."
    exit 0
fi

ls -l

# Execute all sql files in the docker-entrypoint-initdb.d directory
cd /docker-entrypoint-initdb.d
for f in *.sql; do
    echo "Executing $f..."
    mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host "$DB_HOST" < $f
    echo "$f has been executed."
done

echo "All SQL files in docker-entrypoint-initdb.d directory have been executed."

echo "MariaDB has been configured."
exit 0