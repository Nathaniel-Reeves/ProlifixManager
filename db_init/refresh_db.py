import mysqlx
import re
import os
import json

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
                "table_name": "Formula_Details"
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
                    print("\033[0mExecuting SQL statement...")
                    print("\033[0m     ", statement[:60].strip(), "...")
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
            print("\033[32mCommitting the transaction...")
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

    if flag:
        # Load the SQL schema from the file
        print("\033[0mRecreating tables...")
        flag = execute_from_sql("schema.sql", session)

    if flag:
        # Load the SQL views from the file
        print("\033[0mReloading views...")
        flag = execute_from_sql("views.sql", session)

    # if flag:
    #     # Load the SQL stored_procedures from the file
    #     flag = execute_from_sql("stored_procedures.sql", session)

    if flag:
        print("Refresh database schema successful!")
    else:
        print("\033[31mRefresh database schema failed.")

    return flag


def smart_split_csv(csv_string):
    """
    Splits a CSV string into a list of values.

    Args:
    csv_string: A string containing comma-separated values.

    Returns:
    A list of values.
    """
    values = []
    quote_open = False
    current_item = ""

    # Iterate through each character in the CSV string
    for char in csv_string:
        # If the current character is a comma and not inside quotes,
        # add the current item to the list and start a new item
        if char == ',' and not quote_open:
            values.append(current_item.strip())
            current_item = ""
        # If the current character is a quote, toggle the quote_open flag
        # and add the character to the current item
        elif char == '"':
            quote_open = not quote_open
            current_item += char
        # Otherwise, add the character to the current item
        else:
            current_item += char

    # Add the final item to the list
    values.append(current_item.strip())

    # Check each value in the list for "_id" or "NULL" and modify as necessary
    for v in range(len(values)):
        if "_id" in values[v]:
            # If the value contains "_id", convert to a JSON string
            values[v] = json.dumps(values[v].replace('""', ''))
        if values[v] == 'NULL':
            # If the value is "NULL", convert to None
            values[v] = None

    return values


def main():
    # Reload the database
    print("\033[0mReloading the database...")

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

    # Refresh the database schema
    flag = refresh_database_schema(session)
    if not flag:
        session.close()
        exit(0)

    # Loop through each database and CSV file and insert the data
    for database in DATABASES:
        db_name = database["database"]
        print("\033[0m{} data loading...".format(db_name))
        if database["csv_files"]:
            # Start a transaction
            session.start_transaction()
            db = session.get_schema(db_name)
            loaded = True

            for csv_file in database["csv_files"]:
                table_name = csv_file["table_name"]
                table = db.get_table(table_name)

                print("\033[0mLoading CSV for {} file...".format(table_name))
                csv_data = open(os.getcwd() + "/" + csv_file["file"], "r")

                header = csv_data.readline().strip().split(",")
                print(
                    "\033[0mInserting data into the '{}' table...".format(table_name))

                # Loop through each line of the CSV file and insert the data
                for line in csv_data:
                    values = smart_split_csv(line.strip())
                    try:
                        table.insert(header).values(values).execute()
                    except Exception as e:
                        print(
                            "\033[31mInserting failed due to error: {}\033[0m".format(e))
                        loaded = False
                        break

                csv_data.close()
                if loaded:
                    print(
                        "\033[32mCSV for {} file loaded successfully!\033[0m".format(table_name))
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
            print("\033[0mNo CSV files found for {}".format(db_name))

    # Close the connection to the database
    print("\033[0mClosing the connection to the database...")
    session.close()

if __name__ == "__main__":
    main()