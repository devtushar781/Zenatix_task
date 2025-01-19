import os
from dotenv import load_dotenv

from db_helper import DatabaseHandler
from datahandler import DataLoader, DataPreProcessor
from utils import MetricsCalculator, DataReportGenerator, GraphGenerator
from sql_queries import query_dict

load_dotenv()


def fetch_db_config():
    """
    Fetches database configuration from environment variables.

    Returns:
        dict: Database configuration.
    """
    return {
        "database": os.environ.get("DATABASE"),
        "user": os.environ.get("DBUSER"),
        "password": os.environ.get("PASSWORD"),
        "host": os.environ.get("HOST"),
        "port": os.environ.get("PORT"),
    }


def process_data(csv_path: str, table_name: str, db_config: dict):
    """
    Processes CSV data, loads it into a database, and fills missing timestamps.

    Args:
        csv_path (str): Path to the CSV file.
        table_name (str): Name of the database table.
        db_config (dict): Database configuration.

    Returns:
        pd.DataFrame: Processed and filled data.
    """
    loader = DataLoader(csv_path)
    loader.load_data()
    loader.clean_data()

    db_handler = DatabaseHandler(db_config)

    create_table_sql = query_dict.get("create_table_sql").format(table_name=table_name)
    db_handler.create_table(create_table_sql)

    loader.save_to_db(db_handler, table_name)

    data = db_handler.execute_query(
        query_dict.get("fetch_all_data").format(table_name=table_name)
    )

    preprocessor = DataPreProcessor()
    normalized_data = preprocessor.normalize_sensor_values(data, "sensor_value")
    time_series_data = preprocessor.create_time_series(normalized_data, "timestamp")
    return preprocessor.fill_missing_timestamps(
        time_series_data, group_columns=["site_id", "meter_id"]
    )


def output_generator(filled_data, output_path: str):
    """
    Generates output metrics, graphs, and reports from the processed data.

    Args:
        filled_data (pd.DataFrame): Processed data.
        output_path (str): Path to save the output files.
    """
    metrics_calculator = MetricsCalculator()
    metrics = metrics_calculator.calculate_metrics(
        filled_data, ["site_id", "meter_id"], "sensor_value"
    )

    graph_generator = GraphGenerator()
    graph_generator.generate_plots(metrics, f"{output_path}/plots")

    report_generator = DataReportGenerator()
    report_generator.export_to_csv(metrics, f"{output_path}/metrics_report.csv")


if __name__ == "__main__":
    """
    Main entry point of the script. Fetches configurations, processes data,
    and generates outputs.
    """
    db_config = fetch_db_config()
    csv_path = os.environ.get("CSVPATH")
    table_name = os.environ.get("TABLENAME")
    output_path = os.environ.get("OUTPUTPATH")

    filled_data = process_data(
        csv_path=csv_path, table_name=table_name, db_config=db_config
    )
    output_generator(filled_data=filled_data, output_path=output_path)
