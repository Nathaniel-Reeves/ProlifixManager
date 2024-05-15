#!/bin/bash

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
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host 172.10.10.2 -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '$MARIADB_ROOT_PASSWORD' WITH GRANT OPTION;"
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host 172.10.10.2 -e "FLUSH PRIVILEGES;"

echo "Remote access for root user from any host has been granted."

# Execute SQL commands to create the new user
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host 172.10.10.2 -e "CREATE USER '$DB_USER'@'%' IDENTIFIED BY '$DB_PASSWORD';"
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host 172.10.10.2 -e "GRANT ALL PRIVILEGES ON *.* TO '$DB_USER'@'%';"
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host 172.10.10.2 -e "FLUSH PRIVILEGES;"

echo "User $DB_USER has been created and granted all privileges."

# Setup OQGraph engine for Mariadb
# apt update
# apt upgrade -y
# apt-get install mariadb-plugin-oqgraph
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host 172.10.10.2 -e "INSTALL SONAME 'ha_oqgraph';"
mysql -u "root" -p"$MARIADB_ROOT_PASSWORD" --host 172.10.10.2 -e "SHOW ENGINES;"

echo "OQGraph engine is installed."

exit 0