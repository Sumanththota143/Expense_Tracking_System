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


# Function to fetch all rows from expense table
def fetch_all_data():
    connection, mycur = connect_DB()

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
fetch_all_data()
