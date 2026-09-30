import mysql.connector
import logging


# ============================================================
# LOGGING CONFIGURATION
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    filename="D:/OneDrive/Desktop/bootcamp/my_projects/"
             "Expense_Tracking_System/backend/fetch_db.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "expense_data"
}


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    try:

        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )

        logging.info("Database connection successful")

        return connection

    except mysql.connector.Error as error:

        logging.error(
            f"Database connection failed: {error}"
        )

        raise


# ============================================================
# FETCH ALL DATA
# ============================================================

def fetch_all_data():

    logging.info("Fetching all expense data")

    connection = None
    mycur = None

    try:

        connection = get_connection()

        mycur = connection.cursor(
            dictionary=True
        )

        query = """
            SELECT
                id,
                expense_date,
                amount,
                category,
                notes
            FROM expenses
            ORDER BY expense_date DESC, id DESC;
        """

        mycur.execute(query)

        result = mycur.fetchall()

        logging.info(
            f"Fetched {len(result)} expense records"
        )

        return result

    except mysql.connector.Error as error:

        logging.error(
            f"Error fetching all data: {error}"
        )

        raise

    finally:

        if mycur:
            mycur.close()

        if connection:
            connection.close()


# ============================================================
# FETCH DATA BY DATE
# ============================================================

def fetch_by_date(expense_date):

    logging.info(
        f"Fetching expenses for date: {expense_date}"
    )

    connection = None
    mycur = None

    try:

        connection = get_connection()

        mycur = connection.cursor(
            dictionary=True
        )

        query = """
            SELECT
                id,
                expense_date,
                amount,
                category,
                notes
            FROM expenses
            WHERE expense_date = %s
            ORDER BY id ASC;
        """

        mycur.execute(
            query,
            (expense_date,)
        )

        result = mycur.fetchall()

        logging.info(
            f"Found {len(result)} records "
            f"for {expense_date}"
        )

        return result

    except mysql.connector.Error as error:

        logging.error(
            f"Error fetching data by date: {error}"
        )

        raise

    finally:

        if mycur:
            mycur.close()

        if connection:
            connection.close()


# ============================================================
# FETCH ONE EXPENSE BY ID
# ============================================================

def fetch_by_id(expense_id):

    logging.info(
        f"Fetching expense with ID: {expense_id}"
    )

    connection = None
    mycur = None

    try:

        connection = get_connection()

        mycur = connection.cursor(
            dictionary=True
        )

        query = """
            SELECT
                id,
                expense_date,
                amount,
                category,
                notes
            FROM expenses
            WHERE id = %s;
        """

        mycur.execute(
            query,
            (expense_id,)
        )

        result = mycur.fetchone()

        return result

    except mysql.connector.Error as error:

        logging.error(
            f"Error fetching expense by ID: {error}"
        )

        raise

    finally:

        if mycur:
            mycur.close()

        if connection:
            connection.close()


# ============================================================
# INSERT / ADD NEW EXPENSE
# ============================================================

def insert_data(
    expense_date,
    amount,
    category,
    notes
):

    logging.info(
        f"Adding expense | "
        f"date={expense_date}, "
        f"amount={amount}, "
        f"category={category}, "
        f"notes={notes}"
    )

    connection = None
    mycur = None

    try:

        connection = get_connection()

        mycur = connection.cursor(
            dictionary=True
        )

        query = """
            INSERT INTO expenses
            (
                expense_date,
                amount,
                category,
                notes
            )
            VALUES (%s, %s, %s, %s);
        """

        values = (
            expense_date,
            amount,
            category,
            notes
        )

        mycur.execute(
            query,
            values
        )

        connection.commit()

        new_id = mycur.lastrowid

        logging.info(
            f"Expense inserted successfully. "
            f"New ID: {new_id}"
        )

        # Fetch the newly inserted record
        mycur.execute(
            """
            SELECT
                id,
                expense_date,
                amount,
                category,
                notes
            FROM expenses
            WHERE id = %s;
            """,
            (new_id,)
        )

        result = mycur.fetchone()

        return result

    except mysql.connector.Error as error:

        if connection:
            connection.rollback()

        logging.error(
            f"Error inserting expense: {error}"
        )

        raise

    finally:

        if mycur:
            mycur.close()

        if connection:
            connection.close()


# ============================================================
# UPDATE ONE EXPENSE BY ID
# ============================================================

def update_data(
    expense_id,
    expense_date,
    amount,
    category,
    notes
):

    logging.info(
        f"Updating expense ID {expense_id} | "
        f"date={expense_date}, "
        f"amount={amount}, "
        f"category={category}, "
        f"notes={notes}"
    )

    connection = None
    mycur = None

    try:

        connection = get_connection()

        mycur = connection.cursor(
            dictionary=True
        )

        query = """
            UPDATE expenses
            SET
                expense_date = %s,
                amount = %s,
                category = %s,
                notes = %s
            WHERE id = %s;
        """

        values = (
            expense_date,
            amount,
            category,
            notes,
            expense_id
        )

        mycur.execute(
            query,
            values
        )

        connection.commit()

        # No record with this ID
        if mycur.rowcount == 0:

            logging.warning(
                f"Expense ID {expense_id} "
                f"was not found"
            )

            return None

        logging.info(
            f"Expense ID {expense_id} "
            f"updated successfully"
        )

        # Return updated record
        mycur.execute(
            """
            SELECT
                id,
                expense_date,
                amount,
                category,
                notes
            FROM expenses
            WHERE id = %s;
            """,
            (expense_id,)
        )

        result = mycur.fetchone()

        return result

    except mysql.connector.Error as error:

        if connection:
            connection.rollback()

        logging.error(
            f"Error updating expense "
            f"{expense_id}: {error}"
        )

        raise

    finally:

        if mycur:
            mycur.close()

        if connection:
            connection.close()


# ============================================================
# DELETE ONE EXPENSE BY ID
# ============================================================

def delete_data_by_id(expense_id):

    logging.info(
        f"Deleting expense ID: {expense_id}"
    )

    connection = None
    mycur = None

    try:

        connection = get_connection()

        mycur = connection.cursor()

        query = """
            DELETE FROM expenses
            WHERE id = %s;
        """

        mycur.execute(
            query,
            (expense_id,)
        )

        connection.commit()

        deleted = mycur.rowcount > 0

        if deleted:

            logging.info(
                f"Expense ID {expense_id} "
                f"deleted successfully"
            )

        else:

            logging.warning(
                f"Expense ID {expense_id} "
                f"was not found"
            )

        return deleted

    except mysql.connector.Error as error:

        if connection:
            connection.rollback()

        logging.error(
            f"Error deleting expense "
            f"{expense_id}: {error}"
        )

        raise

    finally:

        if mycur:
            mycur.close()

        if connection:
            connection.close()


# ============================================================
# DELETE ALL DATA FOR A DATE
#
# WARNING:
# This deletes EVERY expense for that date.
#
# This is kept as a separate function in case you need it
# for administrative purposes.
# ============================================================

def delete_data_by_date(expense_date):

    logging.warning(
        f"Deleting ALL expenses for date: "
        f"{expense_date}"
    )

    connection = None
    mycur = None

    try:

        connection = get_connection()

        mycur = connection.cursor()

        query = """
            DELETE FROM expenses
            WHERE expense_date = %s;
        """

        mycur.execute(
            query,
            (expense_date,)
        )

        connection.commit()

        deleted_count = mycur.rowcount

        logging.warning(
            f"Deleted {deleted_count} records "
            f"for date {expense_date}"
        )

        return deleted_count

    except mysql.connector.Error as error:

        if connection:
            connection.rollback()

        logging.error(
            f"Error deleting records for "
            f"{expense_date}: {error}"
        )

        raise

    finally:

        if mycur:
            mycur.close()

        if connection:
            connection.close()


# ============================================================
# EXPENSE SUMMARY BY CATEGORY
# ============================================================

def fetch_expenses_summary(
    start_date,
    end_date
):

    logging.info(
        f"Fetching expense summary "
        f"from {start_date} to {end_date}"
    )

    connection = None
    mycur = None

    try:

        connection = get_connection()

        mycur = connection.cursor(
            dictionary=True
        )

        query = """
            SELECT
                category,
                SUM(amount) AS total
            FROM expenses
            WHERE expense_date
            BETWEEN %s AND %s
            GROUP BY category
            ORDER BY total DESC;
        """

        mycur.execute(
            query,
            (
                start_date,
                end_date
            )
        )

        result = mycur.fetchall()

        logging.info(
            f"Found {len(result)} categories "
            f"in summary"
        )

        return result

    except mysql.connector.Error as error:

        logging.error(
            f"Error generating expense summary: "
            f"{error}"
        )

        raise

    finally:

        if mycur:
            mycur.close()

        if connection:
            connection.close()


# ============================================================
# TOTAL EXPENSE FOR A DATE RANGE
# ============================================================

def fetch_total_expenses(
    start_date,
    end_date
):

    logging.info(
        f"Calculating total expenses "
        f"from {start_date} to {end_date}"
    )

    connection = None
    mycur = None

    try:

        connection = get_connection()

        mycur = connection.cursor(
            dictionary=True
        )

        query = """
            SELECT
                COALESCE(SUM(amount), 0) AS total
            FROM expenses
            WHERE expense_date
            BETWEEN %s AND %s;
        """

        mycur.execute(
            query,
            (
                start_date,
                end_date
            )
        )

        result = mycur.fetchone()

        return result

    except mysql.connector.Error as error:

        logging.error(
            f"Error calculating total expenses: "
            f"{error}"
        )

        raise

    finally:

        if mycur:
            mycur.close()

        if connection:
            connection.close()
