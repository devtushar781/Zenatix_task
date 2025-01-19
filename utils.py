import os
from logger import logger


class MetricsCalculator:
    """
    A class for calculating statistical metrics from data.
    """

    @staticmethod
    def calculate_metrics(data, group_columns, value_column):
        """
        Calculates average, maximum, and total values grouped by specified columns.

        Args:
            data (pd.DataFrame): Input data.
            group_columns (list): Columns to group by.
            value_column (str): Column to calculate metrics on.

        Returns:
            pd.DataFrame: Metrics including average, maximum, and total.
        """
        metrics = data.groupby(group_columns).agg(
            {value_column: ["mean", "max", "sum"]}
        )
        metrics.columns = ["average", "maximum", "total"]
        logger.info("Metrics calculation completed.")
        return metrics


class GraphGenerator:
    """
    A class for generating and saving bar plots from metrics data.
    """

    @staticmethod
    def generate_plots(metrics, output_dir):
        """
        Generates bar plots for each metric column and saves them as PNG files.

        Args:
            metrics (pd.DataFrame): Metrics data.
            output_dir (str): Directory to save plots.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for column in metrics.columns:
            plot = metrics[column].plot(kind="bar", title=column)
            fig = plot.get_figure()
            fig.savefig(os.path.join(output_dir, f"{column}.png"))
            fig.clf()

        logger.info("Plots generated and saved.")


class DataReportGenerator:
    """
    A class for exporting metrics data to a CSV file.
    """

    @staticmethod
    def export_to_csv(metrics, file_path):
        """
        Exports metrics data to a CSV file.

        Args:
            metrics (pd.DataFrame): Metrics data.
            file_path (str): Path to save the CSV file.
        """
        metrics.to_csv(file_path)
        logger.info(f"Metrics exported to {file_path}.")
