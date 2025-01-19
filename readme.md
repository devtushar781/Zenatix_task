# Project: Data Processing and Analysis Pipeline

## Overview
This project provides a modular and scalable solution for processing, analyzing, and visualizing sensor data using Python. It includes features such as data loading, cleaning, normalization, database handling, metric calculation, and report generation.

## Features
1. **DataLoader**: Load and clean CSV data, then save it to a PostgreSQL database.
2. **DatabaseHandler**: Handles PostgreSQL database operations (create table, insert data, fetch data).
3. **DataPreProcessor**: Normalize data, create time-series, and handle missing timestamps.
4. **MetricsCalculator**: Compute metrics like average, maximum, and total values.
5. **GraphGenerator**: Generate and save visualizations.
6. **DataReportGenerator**: Export metrics to CSV files.
7. **Docker Support**: Containerized deployment with Docker and Docker Compose.

## Setup Instructions

### Prerequisites
- Python 3.8+
- Docker and Docker Compose
- PostgreSQL
- Required Python packages (see `requirements.txt`)

### Steps to Run

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-folder>s
   ```

2. **Set Environment Variables**
   Create a `.env` file in the root directory with the following variables:
   ```env
   DATABASE=your_database_name
   DBUSER=your_database_user
   PASSWORD=your_database_password
   HOST=db
   PORT=5432
   CSVPATH=data.csv
   TABLENAME=your_table_name
   OUTPUTPATH=result
   ```

3. **Build and Run Using Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access Output**
   Processed data, metrics, plots and logs will be available in the `result` directory.

## File Descriptions

### Python Modules
- `main.py`: Entry point for the application.
- `db_helper.py`: Contains `DbConnector` and `DatabaseHandler` classes.
- `datahandler.py`: Implements `DataLoader` and `DataPreProcessor` classes.
- `utils.py`: Includes `MetricsCalculator`, `GraphGenerator`, and `DataReportGenerator`.
- `sql_queries.py`: SQL query templates.
- `logger` : Handling the logs in pipeline.

### Docker Files
- `Dockerfile`: Builds the application image.
- `docker-compose.yml`: Configures multi-container setup with PostgreSQL and the app.

### Others
- `requirements.txt`: Lists required Python dependencies.



