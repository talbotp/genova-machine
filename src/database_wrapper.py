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
        self.table_name = 'twitter_' + config.RUNTIME_CONFIG['twitter-handle']
        self.create_table()

    def __del__(self):
        self.connection.close()

    # Create table if not there.
    def create_table(self):
        db_name = config.DATABASE_CONFIG['database']

        # First check if the table exists.
        sql_query = '''
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = '{}'
                        AND table_name LIKE '%{}%';
        '''.format(db_name, self.table_name)

        db_cursor = self.connection.cursor(buffered=True)

        if db_cursor.execute(sql_query) is None:
            sql_create = '''
                        CREATE TABLE {} (
                            id_str              VARCHAR(100) PRIMARY KEY,
                            datetime_created    DATETIME,
                            text                VARCHAR(282)
                        );
            '''.format(self.table_name)

            db_cursor.execute(sql_create)

        db_cursor.close()
        return None

    # Insert a single Record into our Twitter table.
    def insert_record(self, id_string, date_time, tweet_text):
        sql_insert = '''
                    INSERT INTO {} (
                        id_str,
                        datetime_created,
                        text)
                    VALUES (
                        %s,
                        %s,
                        %s
                    );
        '''.format(self.table_name)
        val = (id_string, date_time, tweet_text)

        cursor = self.connection.cursor()
        cursor.execute(sql_insert, val)

        self.connection.commit()
        cursor.close()
        return None

    # Insert a List of records in a more efficient way than using insert_record
    # list is a list of tweets as returned by the tweepy API.
    def insert_many_records(self, list):
        sql_insert = '''
                    INSERT INTO {} (
                        id_str,
                        datetime_created,
                        text)
                    VALUES (
                        %s,
                        %s,
                        %s
                    );
        '''.format(self.table_name)
        val = []
        for tweet in list:
            print(tweet.text.encode('utf-8'))
            val.append(
                (tweet.id_str, tweet.created_at, tweet.text.encode('utf-8'))
            )

        cursor = self.connection.cursor()
        cursor.executemany(sql_insert, val)

        self.connection.commit()
        cursor.close()
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
    mysql_use = '''
                USE {};
    '''.format(db_name)

    try:
        db_cursor.execute(mysql_use)
    except mysql.connector.errors.ProgrammingError:
        mysql_create = '''
                        CREATE DATABASE {};
        '''.format(db_name)
        db_cursor.execute(mysql_create)
        db_cursor.execute(mysql_use)
    finally:
        db_cursor.close()

    return db
