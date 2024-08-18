## Append data to the BigQuery table
## Have one table for each sensor type (e.g. BME280)
## Primary Key (Timestamp, BeehiveId/PiId, SensorId)
## Attributes: (Temperature, Humidity, Barometric Pressure)

from google.cloud import bigquery

dataset_name = 'sensor_data'
table_name = 'bme280'

# Construct a BigQuery client object.
client = bigquery.Client()

## Create the table
# Set table_id to the ID of the table to create.
table_id = f"{client.project}.{dataset_name}.{table_name}"

schema = [
    bigquery.SchemaField("timestamp", "INT64", mode="REQUIRED", description="Microseconds after epoch time"),
    bigquery.SchemaField("beehiveid", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("sensorid", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("temperature_f", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("humidity_prcnt", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("barometricpressure_hpa", "FLOAT64", mode="NULLABLE"),
]

table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)  # Make an API request.
print(
    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
)