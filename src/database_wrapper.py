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
        self.set_connected_db()
        self.table_name = 'twitter_' + config.RUNTIME_CONFIG['twitter-handle']

    def __del__(self):
        self.connection.close()

    # Create table if not there.
    def create_table(self):
        db_name = config.DATABASE_CONFIG['database']

        # First check if the table exists.
        sql_check = '''
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = '{}'
                        AND table_name LIKE '%{}%';
        '''.format(db_name, self.table_name)

        db_cursor = self.connection.cursor(buffered=True)

        db_cursor.execute(sql_check)

        # If table doesn't exist then we create it.
        if len(db_cursor.fetchall()) == 0:
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
                    INSERT IGNORE INTO {} (
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

        # Commit the insertion and close cursor.
        self.connection.commit()
        cursor.close()
        return None

    # Insert a List of records in a more efficient way than using insert_record
    # list is a list of tweets as returned by the tweepy API.
    def insert_many_records(self, list_of_tweets):
        sql_insert = '''
                    INSERT IGNORE INTO {} (
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

        for tweet in list_of_tweets:
            # print('{} : {}'.format(tweet.id_str, tweet.text.encode('utf-8')))
            val.append(
                (tweet.id_str, tweet.created_at, tweet.text.encode('utf-8'))
            )

        cursor = self.connection.cursor()
        cursor.executemany(sql_insert, val)

        self.connection.commit()
        cursor.close()
        return None

    # Use this for clean up by dropping our table in the database.
    # THIS IS A HOUSEKEEPING METHOD, LIKELY NEVER TO BE USED IN OUR PROGRAM.
    def delete_table(self):
        sql_drop = '''
                    DROP TABLE IF EXISTS {};
        '''.format(self.table_name)

        db_cursor = self.connection.cursor()
        db_cursor.execute(sql_drop)
        db_cursor.close()
        return None

    # Drop our database.
    # THIS IS A HOUSEKEEPING METHOD, LIKELY NEVER TO BE USED IN OUR PROGRAM.
    def delete_database(self):
        sql_drop = '''
                    DROP DATABASE {};
        '''.format(config.DATABASE_CONFIG['database'])

        db_cursor = self.connection.cursor()
        db_cursor.execute(sql_drop)
        db_cursor.close()
        return None

    # Make a valid connection to a database, if the connection is not valid then
    # we throw an error and close the program. If the database does not exist
    # then we create it.
    def set_connected_db(self):
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

        self.connection = db
        return None
