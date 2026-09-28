import mysql.connector

import logging

#basic configuarion mandatory
logging.basicConfig(
    #set level as 1st logging level
    level=logging.INFO ,
    # by putting a file name all logs are recorded in a file instead of terminal
    filename="D:/OneDrive/Desktop/bootcamp/my_projects/Expense_Tracking_System/backend/fetch_db.log" ,
    # to print the time of log created use:
    format="%(asctime)s - %(levelname)s - %(message)s"

    )


# Function to fetch all rows from expense table
def fetch_all_data():
    logging.info("fetching all data")
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_data"
    )

    mycur = connection.cursor(dictionary=True)

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


# Function to fetch data by date
def fetch_by_date(date):
    logging.info(f"fetching data for date{date}")
    print("started")

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_data"
    )

    mycur = connection.cursor(dictionary=True)

    query = """
        SELECT *
        FROM expenses
        WHERE expense_date = %s;
    """

    # Execute the query
    mycur.execute(query, (date,))

    # Fetch the result
    result = mycur.fetchall()

    if not result:
        logging.warning("date format is incorrect")
        print("no data for this date or incorrect date")
    else:
        # Print the result
        for row in result:
            print(row)

        mycur.close()
        connection.close()

        return result

    mycur.close()
    connection.close()


# Insert data into table
def insert_data(expense_date, amount, category, notes):
    logging.info(f"data inserting with date:{expense_date}\namt:{amount}\ncategory:{category}\nnote:{notes}")
    print("***** INSERT DATA *****")

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_data"
    )

    mycur = connection.cursor(dictionary=True)

    clm_names = ["expense_date", "amount", "category", "notes"]

    data = []

    for i in clm_names:

        # ---------------- DATE ----------------
        if i == "expense_date":

            print("Enter date in YYYY-MM-DD format only")

            ip = expense_date

            if (
                len(ip) != 10
                or not ip[:4].isdigit()
                or ip[4] != "-"
                or not ip[5:7].isdigit()
                or ip[7] != "-"
                or not ip[8:].isdigit()
            ):
                print("Incorrect date entered")

                mycur.close()
                connection.close()

                return "Incorrect date format"

            else:
                data.append(ip)

        # ---------------- CATEGORY ----------------
        if i == "category":

            print("We have the categories:")

            mycur.execute(
                "SELECT DISTINCT category FROM expenses"
            )

            category_list = mycur.fetchall()

            cat_val = []

            for cat in category_list:
                cat_val.append(cat)

            print(cat_val)

            ip = category

            data.append(ip)

        # ---------------- AMOUNT / NOTES ----------------
        if i != "expense_date" and i != "category":

            if i == "amount":
                ip = amount
            else:
                ip = notes

            data.append(ip)

    print("You entered:", data)

    # ---------------- INSERT QUERY ----------------

    query = """
        INSERT INTO expenses (expense_date, amount, category, notes)
        VALUES (%s, %s, %s, %s)
    """

    mycur.execute(query, data)

    connection.commit()

    mycur.close()
    connection.close()

    return "Expense added successfully"


# Delete data by date
def delete_data_by_date(date):
    logging.info(f"deleting data for date{date}")
    print("***** DELETE DATA BY DATE *****")

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_data"
    )

    mycur = connection.cursor(dictionary=True)

    if (
        len(date) == 10
        and date[:4].isdigit()
        and date[4] == "-"
        and date[5:7].isdigit()
        and date[7] == "-"
        and date[8:].isdigit()
    ):

        query = """
            DELETE FROM expenses
            WHERE expense_date = %s;
        """

        mycur.execute(query, (date,))

        connection.commit()

        print("ALL RECORDS ARE DELETED FOR :", date)

    else:

        print("Enter the date in correct format!")

    mycur.close()
    connection.close()


# Function to get sum of all expenses for each category
def fetch_expenses_summary(start_date, end_date):
    logging.info(f"summary for date range {start_date} to {end_date}")
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_data"
    )

    mycur = connection.cursor(dictionary=True)

    query = """
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE expense_date
        BETWEEN %s AND %s
        GROUP BY category;
    """

    mycur.execute(query, (start_date, end_date))

    result = mycur.fetchall()

    for i in result:
        print(i)

    mycur.close()
    connection.close()

