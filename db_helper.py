import psycopg2
import pandas as pd
from psycopg2 import sql
import time
from logger import logger


class DbConnector:
    """
    Handles PostgreSQL database connection with retries.
    """

    def __init__(self, config):
        logger.info(config)
        self.config = config

    def sql_client(self):
        """
        Establishes a database connection with retry logic.
        """
        try_count = 0
        while try_count < 5:
            time.sleep(try_count**2)
            logger.info(f"Try to connect db {try_count} time")
            try:
                return psycopg2.connect(**self.config)
            except Exception as e:
                try_count += 1
                logger.info(f"Error occurred - {e}")


class DatabaseHandler(DbConnector):
    """
    Manages database operations like creating tables, inserting, and querying data.
    """

    def __init__(self, config):
        """
        Initializes the handler and connects to the database.
        """
        super().__init__(config)
        self.client = self.sql_client()

    def create_table(self, create_table_sql):
        """
        Creates a database table using the provided SQL.
        """
        try:
            cursor = self.client.cursor()
            cursor.execute(create_table_sql)
            self.client.commit()
            cursor.close()
            logger.info("Table created successfully.")
        except Exception as e:
            logger.info(f"Error creating table: {e}")

    def insert_data(self, insert_query, data_to_insert):
        """
        Inserts data into the table using the rawsql query.
        """
        try:
            cursor = self.client.cursor()
            insert_query = sql.SQL(insert_query)
            cursor.executemany(insert_query, data_to_insert)
            self.client.commit()
            cursor.close()
            logger.info("Data inserted successfully.")
        except Exception as e:
            logger.info(f"Error inserting data: {e}")

    def execute_query(self, query):
        """
        Executes query and returns the result as a Pandas DataFrame.
        """
        try:
            df = pd.read_sql_query(query, self.client)
            return df
        except Exception as e:
            logger.info(f"Error executing query: {e}")
            return None
