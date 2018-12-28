################################################################################
#
# Here we define a wrapper for our database methods.
#
# We must be careful of SQL injection in the tweets. ie, when we add tweets, we
# must check whether there are
#
# Author: P Talbot
#
################################################################################

import sys
import mysql.connector

from src import config


class DatabaseWrapper:

    def __init__(self):
        self.connection = get_connected_db()
        self.create_table()

    def __del__(self):
        self.connection.close()

    # Create table if not there.
    def create_table(self):
        db_name = config.DATABASE_CONFIG['database']
        handle = config.RUNTIME_CONFIG['twitter-handle']

        # First check if the table exists.
        sql_query = '''
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = '{}'
                    AND table_name LIKE '%{}%';
                '''.format(db_name, handle)
        print(sql_query)

        db_cursor = self.connection.cursor(buffered=True)

        print(db_cursor.execute(sql_query))

        if db_cursor.execute(sql_query) is None:
            sql_create = '''
                    CREATE TABLE {} (
                        id_str              VARCHAR(100) PRIMARY KEY,
                        datetime_created    DATETIME,
                        text                VARCHAR(282)
                    )
                    '''.format(handle)
            print(sql_create)

            db_cursor.execute(sql_create)

        db_cursor.close()
        return None


# Make a valid connection to a database, if the connection is not valid then we
# throw an error and close the program. If the database does not exist then we
# create it.
def get_connected_db():
    try:
        db = mysql.connector.connect(
            host=config.DATABASE_CONFIG['host'],
            user=config.DATABASE_CONFIG['user'],
            passwd=config.DATABASE_CONFIG['passwd']
        )
    except mysql.connector.errors.InterfaceError:
        sys.exit('That is not a valid host name for the database.')
    except mysql.connector.errors.ProgrammingError:
        sys.exit('That is not a valid username or password for the database.')

    db_cursor = db.cursor()
    db_name = config.DATABASE_CONFIG['database']
    mySQL_use = '''
            USE {};
            '''.format(db_name)

    try:
        db_cursor.execute(mySQL_use)
    except mysql.connector.errors.ProgrammingError:
        mySQL_create = '''
                CREATE DATABASE {};
                '''.format(db_name)
        db_cursor.execute(mySQL_create)
        db_cursor.execute(mySQL_use)
    finally:
        db_cursor.close()

    return db
