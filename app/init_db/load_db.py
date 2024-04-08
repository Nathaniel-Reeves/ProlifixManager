# sudo apt install libmariadb3 libmariadb-dev
# pip3 install mariadb

import mariadb
import re
import os
from os.path import exists
import csv
import sys
from dotenv import load_dotenv

# Define the connection details
# DB_HOST = os.environ.get('DB_HOST')
# if DB_HOST is None:
#     # Change Host for testing purposes
#     #DB_HOST = '127.0.0.1'
#     DB_HOST = '192.168.1.133'

# DB_PORT = os.environ.get('DB_PORT')
# if DB_PORT is None:
#     DB_PORT = '3306'

# DB_USER = os.environ.get('DB_USERNAME')
# if DB_USER is None:
#     DB_USER = 'client'

# DB_PASSWORD = os.environ.get('DB_PASSWORD')
# if DB_PASSWORD is None:
#     DB_PASSWORD = "ClientPassword!5"

parent_dir = os.path.dirname(os.path.realpath(__file__))

def print_config():
    print()
    print("App Configurations:")
    for v in env_variables:
        print(f"    {v[0]}: {v[1]}")
    print()
    print()

# Set env variables
print("Loading Environment Variables")
app_dir = os.path.split(parent_dir)[0]
print(f"Env Location: ", os.path.join(app_dir,".env"))
load_dotenv(os.path.join(app_dir,".env"), override=True)
env_variables = os.environ.items()
print_config()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# Define the databases and their corresponding CSV files
DATABASES = [
    {
        "database": "Organizations",
        "csv_files": [
            {
                "file": "./csv_data/Organizations/Organizations db - Organizations.csv",
                "table_name": "Organizations"
            },
            {
                "file": "./csv_data/Organizations/Organizations db - Organization_Names.csv",
                "table_name": "Organization_Names"
            },
            {
                "file": "./csv_data/Organizations/Organizations db - People.csv",
                "table_name": "People"
            },
            {
                "file": "./csv_data/Organizations/Organizations db - Users.csv",
                "table_name": "Users"
            },
            {
                "file": "./csv_data/Organizations/Organizations db - Facilities.csv",
                "table_name": "Facilities"
            }
        ]
    },
    {
        "database": "Products",
        "csv_files": [
            {
                "file": "./csv_data/Products/Products db - Product_Master.csv",
                "table_name": "Product_Master"
            }
        ]
    },
    {
        "database": "Manufacturing",
        "csv_files": [
            {
                "file": "./csv_data/Manufacturing/Manufacturing db - Processes.csv",
                "table_name": "Processes"
            }
        ]
    },
    {
        "database": "Inventory",
        "csv_files": [
            {
                "file": "./csv_data/Inventory/Inventory - Components.csv",
                "table_name": "Components"
            },
            {
                "file": "./csv_data/Inventory/Inventory - Component_Names.csv",
                "table_name": "Component_Names"
            },
            {
                "file": "./csv_data/Inventory/Inventory - Item_id.csv",
                "table_name": "Item_id"
            },
            {
                "file": "./csv_data/Inventory/Inventory - Inventory.csv",
                "table_name": "Inventory"
            }
        ]
    },
    {
        "database": "Orders",
        "csv_files": [
            {
                "file": "./csv_data/Orders/Orders db - Sales_Orders.csv",
                "table_name": "Sales_Orders"
            },
            {
                "file": "./csv_data/Orders/Orders db - Sale_Order_Detail.csv",
                "table_name": "Sale_Order_Detail"
            },
            {
                "file": "./csv_data/Orders/Orders db - Lot_Numbers.csv",
                "table_name": "Lot_Numbers"
            },
            {
                "file": "./csv_data/Orders/Orders db - Purchase_Orders.csv",
                "table_name": "Purchase_Orders"
            },
            {
                "file": "./csv_data/Orders/Orders db - Purchase_Order_Detail.csv",
                "table_name": "Purchase_Order_Detail"
            }
        ]
    },
    {
        "database": "Inventory",
        "csv_files": [
            {
                "file": "./csv_data/Inventory/Inventory - Inventory_Log.csv",
                "table_name": "Inventory_Log"
            }
        ]
    },
    {
        "database": "Formulas",
        "csv_files": [
            {
                "file": "./csv_data/Formulas/Formulas - Formula_Master.csv",
                "table_name": "Formula_Master"
            },
            {
                "file": "./csv_data/Formulas/Formulas - Formula_Detail.csv",
                "table_name": "Formula_Detail"
            }
        ]
    }
]


def execute_from_sql(file_name, session):
    """
    Executes SQL statements from a file and returns True if successful,
    False otherwise. Uses the provided session to execute the statements.

    Args:
    file_name (str): The name of the file containing the SQL statements.
    session: An instance of a database session.

    Returns:
    bool: True if successful, False otherwise.
    """
    flag = False
    # Start a transaction
    print("\033[0mStarting a transaction...")
    # session.start_transaction()

    # Load the SQL file
    print("\033[0mLoading the SQL file: {}".format(file_name))
    with open(file_name, "r") as f:
        print("\033[0mExecuting SQL statements from file: {}".format(file_name))
        try:
            # Execute each SQL statement in the file
            statement = ""
            function_flag = False
            cur = session.cursor()
            for line in f:
                if re.match(r'--', line):
                    # Ignore comments
                    continue

                if re.match(r'DELIMITER ~~', line):
                    print("Delimiter change!  DELIMITER ~~")
                    function_flag = True
                    continue

                if re.match(r'~~', line) and function_flag:
                    print("End Temporary Delimiter change!")
                    function_flag = False
                    # print("\033[0mExecuting SQL statement...")
                    # print("\033[0m     ", statement[:60].strip(), "...")
                    cur.execute(statement)
                    statement = ""
                    continue

                if re.match(r'DELIMITER ;', line):
                    function_flag = False
                    statement = ""
                    continue

                if not function_flag:
                    if not re.search(r';$', line):
                        # Add the line to the current statement
                        statement = statement + line
                    else:
                        # Execute the complete SQL statement
                        statement = statement + line
                        # print("\033[0mExecuting SQL statement...")
                        # print("\033[0m     ", statement[:60].strip(), "...")
                        cur.execute(statement)
                        statement = ""
                else:
                    statement = statement + line

        except Exception as e:
            # Rollback the transaction in case of an error
            print("\033[31mRolling back the transaction due to an error...")
            session.rollback()

            # Print the error for debugging
            print("\033[31mAn error occurred: {}".format(e))
            print("\033[31mStopped near: \n{}\n".format(statement))
            print()

        else:
            # Commit the transaction
            print("\033[32mExecution successful!")
            session.commit()
            print("\033[0mCommitting the transaction...")
            flag = True

    return flag

def refresh_database_schema(session):
    """
    Refreshes a single database schema by dropping existing tables, recreating them,
    and reloading views. Uses the provided session to execute SQL statements.

    Args:
    session: An instance of a database session.

    Returns:
    bool: True if successful, False otherwise.
    """
    flag = True

    # Print working directory to console
    working_dir = os.getcwd()
    print("Working Directory: ", working_dir)
    print("ls :", os.listdir())

    if flag:
        # Load the SQL drop_order from the file
        print("\033[0mDropping existing tables...")
        flag = execute_from_sql("./schema/drop_order.sql", session)
        print()

    if flag:
        # Load the SQL schema from the file
        print("\033[0mRecreating tables...")
        flag = execute_from_sql("./schema/schema.sql", session)
        print()

    if flag:
        # Load the SQL views from the file
        print("\033[0mReloading views...")
        flag = execute_from_sql("./schema/views.sql", session)
        print()

    if flag:
        # Load the SQL sys_functions from the file
        print("\033[0mReloading sys_functions...")
        flag = execute_from_sql(
            "./schema/sys_functions.sql", session)
        print()

    if flag:
        print("\033[32mRefresh database schema successful!")

    else:
        print("\033[31mRefresh database schema failed.")
    print()

    return flag


def delete_database_schema(session):
    """
    Drops all databasess.

    Args:
    session: An instance of a database session.

    Returns:
    bool: True if successful, False otherwise.
    """
    flag = True

    if flag:
        # Load the SQL drop_order from the file
        print("\033[0mDropping existing tables...")
        flag = execute_from_sql("./schema/drop_order.sql", session)
        print()

    if flag:
        print("\033[32mDrop all databases successful!")

    else:
        print("\033[31mDrop all databases failed.")
    print()

    return flag

def main(force=False, drop_databases=False):

    print("\033[0mStarting Program...")
    # Handle Force Run Overide Argument
    if not force:
        try:
            if not force:
                force = sys.argv[1] == "force"
            else:
                force = True
        except IndexError:
            force = False

    if not drop_databases:
        try:
            if not drop_databases:
                drop_databases = sys.argv[2] == "drop_databases"
            else:
                drop_databases = True
        except IndexError:
            drop_databases = False

    if not force:
        file_exists = exists(
            "init_db_flag_do_not_delete.txt")
        if file_exists:
            print(
                "\033[31minit_db_flag_do_not_delete.txt already exists. Exiting...\033[0m")
            sys.exit(0)
        else:
            print(
                "\033[31minit_db_flag_do_not_delete.txt does not exist. \033[0m")
            print("Continueing...")
    else:
        print("Database Refresh Forced!")
        print("I hope you know what you are doing...")

    # Reload the database

    # Display the connection details
    print("\033[0mConnection Details:")
    print("\033[0m    Host: {}".format(DB_HOST))
    print("\033[0m    Port: {}".format(DB_PORT))
    print("\033[0m    User: {}".format(DB_USER))
    print("\033[0m    Password: {}".format(DB_PASSWORD))

    # Comment this line for debugging connection
    check = input("Are these credentials correct (Y/N)?\n")
    # check = "y"

    print()
    if check.lower() != "y":
        print("\033[31mExiting...\033[0m")
        exit(0)

    # Connect to the database
    print("\033[0mConnecting to the database...")
    try:
        session = mariadb.connect(
            host=DB_HOST,
            port=int(DB_PORT),
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("\033[32mConnection Successful!\033[0m")
        print()
    except Exception as e:
        print("\033[31mConnection Failed!\033[0m")
        print()
        print(e)
        print()
        sys.exit(1)

    # Delete the database if drop_database is True
    if drop_databases:
        flag = delete_database_schema(session)
        if flag:
            print("\033[32mDropped databases successfully!\033[0m")
            print()
        else:
            print("\033[31mDropping databases failed!\033[0m")
            print()
        print("\033[31mExiting...\033[0m")
        session.close()
        return

    # Refresh the database schema
    flag = refresh_database_schema(session)
    if not flag:
        print("\033[31mExiting...\033[0m")
        session.close()
        return
    else:
        print("loading fresh data into new databases...\033[0m")
        print()

    # Loop through each database and CSV file and insert the data
    for database in DATABASES:
        db_name = database["database"]
        print("\033[0m{} data loading...".format(db_name))
        if database["csv_files"]:
            # Start a transaction
            # session.start_transaction()
            loaded = True

            for csv_file in database["csv_files"]:
                table_name = csv_file["table_name"]

                print("\033[0mLoading CSV for {} file...".format(table_name))
                file = open(os.getcwd() + "/" +
                            csv_file["file"], newline='')
                data = list(csv.DictReader(file))

                print(
                    "\033[0mInserting data into the '{}' table...".format(table_name))

                # Loop through each line of the CSV file and insert the data
                for line in data:
                    try:
                        cur = session.cursor()
                        row = list(line.values())
                        for i in range(len(row)):
                            if "_id" in row[i]:
                                row[i] = row[i].replace('"', '\\"')

                        values = '"' + '", "'.join(row) + '"'
                        values = values.replace('"NULL"', 'NULL')

                        headers = ', '.join(list(line.keys()))

                        query = 'INSERT INTO `{}`.`{}` ({}) VALUES ({})'.format(
                            db_name, table_name, headers, values)
                        cur.execute(query)

                    except Exception as e:
                        print(
                            "\033[31mInserting failed due to error: {}\033[0m".format(e))
                        print(query)
                        loaded = False
                        break

                file.close()
                if loaded:
                    print(
                        "\033[32mCSV '{}' file loaded successfully!\033[0m".format(table_name))
                else:
                    break

            # Commit or rollback the transaction based on the success of the data loading
            if loaded:
                print(
                    "\033[32m{} data successfully loaded!\033[0m".format(db_name))
                session.commit()
            else:
                print(
                    "\033[31mCSV for {} file failed to load!\033[0m".format(table_name))
                session.rollback()
        else:
            print("\033[31mNo CSV files found for {}".format(db_name))
        print()

    # Close the connection to the database
    print("\033[0mClosing the connection to the database...")
    session.close()

    # Create a flag file to indicate that the database has been initialized
    file = open("init_db_flag_do_not_delete.txt", "w")
    file.close()
    print("\033[32mDatabase initialized successfully!\033[0m")
    # working_dir = os.getcwd()
    # print("Working Directory: ", working_dir)
    # print("ls :", os.listdir())
    print()
    print("\033[31mExiting...\033[0m")


if __name__ == "__main__":
    main()
