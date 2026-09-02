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

# fetch_data_by_date()

# insert data into table 
def insert_data():
    clm_names = ["expense_date", "amount", "category", "notes"]
    data = [ ]
    for i in clm_names:
        if i == "expense_date":
            print("enter date in YYYY-MM-DD format only")
        if i == "expense_date":
            ip = input(f"enter the data for ({i}): ")
            if len(ip) != 10 and ip[:4].isdigit() and ip[4] != "-" and ip[5:7].isdigit() and ip[7] != "-" and ip[8:].isdigit() :
                print("incorrect date entered")
                break
            else:
                data.append(ip)
        if i != "expense_date":
            ip = input(f"enter the data for ({i}): ")
            data.append(ip)
    print("you entered: ",data)
    query = '''
        INSERT INTO expenses (expense_date, amount, category, notes)
        VALUES (%s, %s, %s, %s);
    '''
    mycur.execute(query,data)
    connection.commit()
    print("enter same date of expense again:")
    fetch_data_by_date()
    
    mycur.close()
    connection.close()

# insert_data()

#delete data by date
def delete_data_by_date():
    date = input("enter date to delete records: ")
    if len(date) == 10 and date[:4].isdigit() and date[4] == "-" and date[5:7].isdigit() and date[7] == "-" and date[8:].isdigit() :
        query = '''
            DELETE FROM expenses
            WHERE expense_date = %s;
        '''
        mycur.execute(query,(date,))
        connection.commit()
        print("ALL RECORDS ARE DELETED FOR :", date)
        mycur.close()
        connection.close()
    else:
        print("Enter the date in correct format!")
        delete_data_by_date()

delete_data_by_date()