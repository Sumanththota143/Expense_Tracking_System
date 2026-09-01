import mysql.connector


# Making connection
def connect_DB():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_data"
    )

    # Create a cursor
    mycur = connection.cursor(dictionary=True)
    return connection, mycur

connection, mycur = connect_DB()
# Function to fetch all rows from expense table
def fetch_all_data():
    query = """
        SELECT *
        FROM expenses;
    """

    # Execute the query
    mycur.execute(query)
    # Fetch the result
    result = mycur.fetchall()

    # Print the result
    for row in result:
        print(row)

    # Close cursor and connection
    mycur.close()
    connection.close()


# Call the function
#fetch_all_data()

def fetch_data_by_date():
    print("Enter the date to fetch records\nNOTE: ENTER IN (YYYY-MM-DD) FORMAT ONLY")
    date = input("enter here: ")
    if len(date) == 10 and date[:4].isdigit() and date[4] == "-" and date[5:7].isdigit() and date[7] == "-" and date[8:].isdigit() :
        query = """
            SELECT *
            FROM expenses
            WHERE expense_date = %s ;
        """

        # Execute the query
        mycur.execute(query,(date,))
        # Fetch the result
        result = mycur.fetchall()
        if not result:
            print("no data for this date or incorrect date")
            var = input("type 'y' to enter date again or 'n' to exit: ")
            if var == "y":
                fetch_data_by_date()
        else:
            # Print the result
            for row in result:
                print(row)

            # Close cursor and connection
            mycur.close()
            connection.close()
    else:
        print("date format is incorrect\nenter in yyyy-mm-dd format only")
        fetch_data_by_date()

fetch_data_by_date()
