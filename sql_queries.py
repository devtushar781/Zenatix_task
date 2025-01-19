query_dict = {
    "create_table_sql":"""CREATE TABLE IF NOT EXISTS {table_name} (
        site_id TEXT,
        meter_id TEXT,
        timestamp TEXT,
        sensor_name TEXT,
        sensor_value REAL,
        status TEXT
    )""",
    "fetch_all_data":"""SELECT * FROM {table_name}""",
    "insert_table_data":("""
    INSERT INTO {table_name} (site_id, meter_id, timestamp, sensor_name, sensor_value, status) 
    VALUES (%s, %s, %s, %s, %s, %s)
"""),

}
