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

    print("*****FETCH ALL DATA*****")

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


# func to fetch data by date
def fetch_by_date(date):
    if len(date) == 10 and date[:4].isdigit() and date[4] == "-" and date[5:7].isdigit() and date[7] == "-" and date[8:].isdigit():
        query = """
            SELECT *
            FROM expenses
            WHERE expense_date = %s ;
        """
        # Execute the query
        mycur.execute(query, (date,))
        # Fetch the result
        result = mycur.fetchall()
        if not result:
            print("no data for this date or incorrect date")
        else:
            # Print the result
            for row in result:
                print(row)
            return result
        mycur.close()
        connection.close()
    else:
        print("INCORRECT DATE FORMAT ENTERED")


# insert data into table
def insert_data(expense_date, amount, category, notes):
    print("*****INSERT DATA*****")
    clm_names = ["expense_date", "amount", "category", "notes"]
    data = []
    for i in clm_names:
        if i == "expense_date":
            print("enter date in YYYY-MM-DD format only")
        if i == "expense_date":
            ip = expense_date
            if len(ip) != 10 and ip[:4].isdigit() and ip[4] != "-" and ip[5:7].isdigit() and ip[7] != "-" and ip[8:].isdigit():
                print("incorrect date entered")
                break
            else:
                data.append(ip)
        if i == "category":
            print("we have the catrgories:")
            category_list = mycur.execute("SELECT DISTINCT category FROM expenses").fetchall()
            cat_val = []
            for i in category_list:
                cat_val.append(i)
            print(cat_val)
            ip = category
            data.append(ip)
        if i != "expense_date" and i != "category":
            if i == "amount":
                ip = amount
            else:
                ip = notes
            data.append(ip)
    print("you entered: ", data)
    query = '''
        INSERT INTO expenses (expense_date, amount, category, notes)
        VALUES (%s, %s, %s, %s);
    '''
    mycur.execute(query, data)
    connection.commit()
    print("enter same date of expense again:")
    fetch_by_date(expense_date)
    mycur.close()
    connection.close()


# delete data by date
def delete_data_by_date(date):
    print("*****DELETE DATA BY DATE*****")
    if len(date) == 10 and date[:4].isdigit() and date[4] == "-" and date[5:7].isdigit() and date[7] == "-" and date[8:].isdigit():
        query = '''
            DELETE FROM expenses
            WHERE expense_date = %s;
        '''
        mycur.execute(query, (date,))
        connection.commit()
        print("ALL RECORDS ARE DELETED FOR :", date)
        mycur.close()
        connection.close()
    else:
        print("Enter the date in correct format!")



# fucntion to get sum of all expenses for each category
def fetch_expenses_summary(start_date, end_date):
    query = '''
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE expense_date
        BETWEEN %s and %s
        GROUP BY category;
    '''
    mycur.execute(query, (start_date, end_date))
    result = mycur.fetchall()
    for i in result:
        print(i)


# function call's

# fetch_all_data()

# fetch_by_date('2026-08-26')

# insert_data('2026-08-26', 500, 'Food', 'Lunch')

# delete_data_by_date('2026-08-26')

# function call code for fetch_expenses_summary

# start_date = input("enter the start date in YYYY-MM-DD format: ")
# if len(start_date) == 10 and start_date[:4].isdigit() and start_date[4] == "-" and start_date[5:7].isdigit() and start_date[7] == "-" and start_date[8:].isdigit() :
#     end_date = input("enter end date in YYYY-MM-DD format: ")
#     if len(start_date) == 10 and start_date[:4].isdigit() and start_date[4] == "-" and start_date[5:7].isdigit() and start_date[7] == "-" and start_date[8:].isdigit() :
#         print(f"start date is {start_date} and end date is {end_date}")
#         fetch_expenses_summary(start_date,end_date)
#     else:
#         print("INCORRECT ENTRY FOR END DATE ")
# else:
#     print("INCORRECT ENTRY FOR START DATE ")