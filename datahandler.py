import pandas as pd
from sql_queries import query_dict
from logger import logger


class DataLoader:
    """
    Loads, cleans, and saves data from a CSV file to a database.
    """

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.data = None

    def load_data(self):
        """
        Loads data from the specified CSV file.
        """
        try:
            self.data = pd.read_csv(self.csv_path)
            logger.info("Data loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")

    def clean_data(self):
        """
        Cleans the loaded data by handling missing values and invalid readings.
        """
        if self.data is None:
            raise ValueError("No data loaded to clean.")

        self.data.dropna(inplace=True)
        self.data = self.data[self.data["sensor_value"] >= 0]
        logger.info("Data cleaning completed.")

    def save_to_db(self, db_handler, table_name):
        """
        Saves cleaned data to the specified database table.
        """
        if self.data is None:
            raise ValueError("No data to save to the database.")
        data = [tuple(x) for x in self.data.to_records(index=False)]
        db_handler.insert_data(
            query_dict.get("insert_table_data").format(table_name=table_name), data
        )
        logger.info(f"Data saved to table {table_name}.")


class DataPreProcessor:
    """
    Provides methods for processing and normalizing data.
    """

    @staticmethod
    def normalize_sensor_values(data, column_name):
        """
        Normalizes sensor values in the specified column.
        """
        data[column_name] = (data[column_name] - data[column_name].min()) / (
            data[column_name].max() - data[column_name].min()
        )
        logger.info("Normalization completed.")
        return data

    @staticmethod
    def create_time_series(data, timestamp_column):
        """
        Converts a DataFrame into a time-series DataFrame indexed by timestamps.
        """
        data[timestamp_column] = pd.to_datetime(data[timestamp_column])
        data.set_index(timestamp_column, inplace=True)
        logger.info("Time-series DataFrame created.")
        return data

    @staticmethod
    def fill_missing_timestamps(data, group_columns):
        """
        Fills missing timestamps with interpolated values for each group.
        """
        filled_data = []
        for _, group in data.groupby(group_columns):
            group = group[~group.index.duplicated(keep="first")]
            group = group.resample("5T").interpolate()
            filled_data.append(group)
        logger.info("Missing timestamps filled with interpolated values.")
        return pd.concat(filled_data)
