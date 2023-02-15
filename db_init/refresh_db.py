import mysqlx
import re
import os
import csv

# Define the connection details
HOST = '192.168.1.42'  # Office
# HOST = '64.255.82.22'  # Home
PORT = 33060
USER = 'client'
PASSWORD = 'clientPassword5!'

# Define the databases and their corresponding CSV files
DATABASES = [
    {
        "database": "Organizations",
        "csv_files": [
            {
                "file": "scv_data/Organizations/Organizations db - Organizations.csv",
                    "table_name": "Organizations"
            },
            {
                "file": "scv_data/Organizations/Organizations db - Organization_Names.csv",
                "table_name": "Organization_Names"
            },
            {
                "file": "scv_data/Organizations/Organizations db - People.csv",
                "table_name": "People"
            },
            {
                "file": "scv_data/Organizations/Organizations db - Users.csv",
                "table_name": "Users"
            },
            {
                "file": "scv_data/Organizations/Organizations db - Facilities.csv",
                "table_name": "Facilities"
            }
        ]
    },
    {
        "database": "Inventory",
        "csv_files": [
            {
                "file": "scv_data/Inventory/Inventory - Components.csv",
                "table_name": "Components"
            },
            {
                "file": "scv_data/Inventory/Inventory - Component_names.csv",
                "table_name": "Component_Names"
            }
        ]
    },
    {
        "database": "Products",
        "csv_files": [
            {
                "file": "scv_data/Products/Products db - Product_Master.csv",
                "table_name": "Product_Master"
            }
        ]
    },
    {
        "database": "Manufacturing",
        "csv_files": [
        ]
    },
    {
        "database": "Orders",
        "csv_files": [
            {
                "file": "scv_data/Orders/Orders db - Purchase_Orders.csv",
                "table_name": "Purchase_Orders"
            },
            {
                "file": "scv_data/Orders/Orders db - Purchase_Orders_Detail.csv",
                "table_name": "Purchase_Orders_Detail"
            },
            {
                "file": "scv_data/Orders/Orders db - Lot_Numbers.csv",
                "table_name": "Lot_Numbers"
            }
        ]
    },
    {
        "database": "Formulas",
        "csv_files": [
            {
                "file": "scv_data/Formulas/Formulas - Formula_Master.csv",
                "table_name": "Formula_Master"
            },
            {
                "file": "scv_data/Formulas/Formulas - Formula_Detail.csv",
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
    session.start_transaction()

    # Load the SQL file
    print("\033[0mLoading the SQL file: {}".format(file_name))
    with open(file_name, "r") as f:
        print("\033[0mExecuting SQL statements from file: {}".format(file_name))
        try:
            # Execute each SQL statement in the file
            statement = ""
            for line in f:
                if re.match(r'--', line):
                    # Ignore comments
                    continue
                if not re.search(r';$', line):
                    # Add the line to the current statement
                    statement = statement + line
                else:
                    # Execute the complete SQL statement
                    statement = statement + line
                    # print("\033[0mExecuting SQL statement...")
                    # print("\033[0m     ", statement[:60].strip(), "...")
                    session.sql(statement).execute()
                    statement = ""

        except Exception as e:
            # Rollback the transaction in case of an error
            print("\033[31mRolling back the transaction due to an error...")
            session.rollback()

            # Print the error for debugging
            print("\033[31mAn error occurred: {}".format(e))
            print("\033[31mStopped near: \n{}\n".format(statement))

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

    if flag:
        # Load the SQL drop_order from the file
        print("\033[0mDropping existing tables...")
        flag = execute_from_sql("drop_order.sql", session)
        print()

    if flag:
        # Load the SQL schema from the file
        print("\033[0mRecreating tables...")
        flag = execute_from_sql("schema.sql", session)
        print()

    if flag:
        # Load the SQL views from the file
        print("\033[0mReloading views...")
        flag = execute_from_sql("views.sql", session)
        print()

    # if flag:
    #     # Load the SQL stored_procedures from the file
    #     flag = execute_from_sql("stored_procedures.sql", session)

    if flag:
        print("\033[32mRefresh database schema successful!")

    else:
        print("\033[31mRefresh database schema failed.")
    print()


    return flag

def main():
    # Reload the database
    print("\033[0mStarting Program...")

    # Display the connection details
    print("\033[0mConnection Details:")
    print("\033[0m    Host: {}".format(HOST))
    print("\033[0m    Port: {}".format(PORT))
    print("\033[0m    User: {}".format(USER))
    print("\033[0m    Password: {}".format(PASSWORD))
    check = input("Are these credentials correct (Y/N)?\n")
    print()
    if check.lower() != "y":
        print("\033[31mExiting...\033[0m")
        exit(0)

    # Connect to the database
    print("\033[0mConnecting to the database...")
    session = mysqlx.get_session(
        {
            "host": HOST,
            "port": PORT,
            "user": USER,
            "password": PASSWORD
        }
    )
    print("\033[32mConnection Successful!\033[0m")
    print()

    # Refresh the database schema
    flag = refresh_database_schema(session)
    if not flag:
        print("\033[31mExiting...\033[0m")
        session.close()
        exit(0)
    else:
        print("loading fresh data into new databases...\033[0m")
        print()

    # Loop through each database and CSV file and insert the data
    for database in DATABASES:
        db_name = database["database"]
        print("\033[0m{} data loading...".format(db_name))
        if database["csv_files"]:
            # Start a transaction
            session.start_transaction()
            loaded = True

            for csv_file in database["csv_files"]:
                table_name = csv_file["table_name"]

                print("\033[0mLoading CSV for {} file...".format(table_name))
                file = open(os.getcwd() + "/" +
                                csv_file["file"], newline='')
                data = list(csv.DictReader(file))

                print("\033[0mInserting data into the '{}' table...".format(table_name))

                # Loop through each line of the CSV file and insert the data
                for line in data:
                    try:
                        row = list(line.values())
                        for i in range(len(row)):
                            if "_id" in row[i]:
                                row[i] = row[i].replace('"','\\"')

                        values = '"' + '", "'.join(row) + '"'
                        values = values.replace('"NULL"', 'NULL')

                        headers = ', '.join(list(line.keys()))

                        query = 'INSERT INTO `{}`.`{}` ({}) VALUES ({})'.format(
                            db_name, table_name, headers, values)
                        session.sql(query).execute()

                    except Exception as e:
                        print(
                            "\033[31mInserting failed due to error: {}\033[0m".format(e))
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

if __name__ == "__main__":
    main()