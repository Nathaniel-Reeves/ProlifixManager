#!/bin/sh

# Read the configuration file
CONFIG_FILE="/conf/config.ini"
DB_USER=$(python -c "import configparser; config = configparser.ConfigParser(); config.read('${CONFIG_FILE}'); print(config['client']['user'])")
DB_PASSWORD=$(python -c "import configparser; config = configparser.ConfigParser(); config.read('${CONFIG_FILE}'); print(config['client']['password'])")
DB_NAME=$(python -c "import configparser; config = configparser.ConfigParser(); config.read('${CONFIG_FILE}'); print(config['database']['name'])")

# Check if the marker file exists
if [ ! -f /marker ]; then
  # Load data into the database
  python /app/load_data.py --user $DB_USER --password $DB_PASSWORD --dbname $DB_NAME

  # Create the marker file
  touch /marker
fi

# Run the command passed to the entrypoint
exec "$@"