# https://stackoverflow.com/questions/71209828/python-bigquery-storage-write-retry-strategy-when-writing-to-default-stream
# Stream data into BigQuery using the new Storage Write API: https://cloud.google.com/bigquery/docs/write-api#python_client
# Requires streaming data using protobuf messages
# Requires installation of protoc: https://grpc.io/docs/protoc-installation/
# Run `protoc --python_out=. bme280.proto` to create the necessary proto python file

from itertools import islice

from google.cloud import bigquery_storage_v1
from google.cloud.bigquery_storage_v1 import types
from google.cloud.bigquery_storage_v1 import writer
from google.protobuf import descriptor_pb2

import bme280_pb2

import logging
import time
logging.basicConfig(level=logging.DEBUG)

CHUNK_SIZE = 2 # Maximum number of rows to use in each AppendRowsRequest.

def chunks(l, n):
    """Yield successive `n`-sized chunks from `l`."""
    _it = iter(l)
    while True:
        chunk = [*islice(_it, 0, n)]
        if chunk:
            yield chunk
        else:
            break


def create_stream_manager(project_id, dataset_id, table_id, write_client):
    # Use the default stream
    # The stream name is:
    # projects/{project}/datasets/{dataset}/tables/{table}/_default

    parent = write_client.table_path(project_id, dataset_id, table_id)
    stream_name = f'{parent}/_default'

    # Create a template with fields needed for the first request.
    request_template = types.AppendRowsRequest()

    # The initial request must contain the stream name.
    request_template.write_stream = stream_name

    # So that BigQuery knows how to parse the serialized_rows, generate a
    # protocol buffer representation of our message descriptor.
    proto_schema = types.ProtoSchema()
    proto_descriptor = descriptor_pb2.DescriptorProto()
    bme280_pb2.BME280.DESCRIPTOR.CopyToProto(proto_descriptor)
    proto_schema.proto_descriptor = proto_descriptor
    proto_data = types.AppendRowsRequest.ProtoData()
    proto_data.writer_schema = proto_schema
    request_template.proto_rows = proto_data

    # Create an AppendRowsStream using the request template created above.
    append_rows_stream = writer.AppendRowsStream(write_client, request_template)

    return append_rows_stream


def send_rows_to_bq(project_id, dataset_id, table_id, write_client, rows):
    # TODO: Implement retry strategy if the API call fails
    append_rows_stream = create_stream_manager(project_id, dataset_id, table_id, write_client)

    response_futures = []

    row_count = 0

    # Send the rows in chunks, to limit memory usage.

    for chunk in chunks(rows, CHUNK_SIZE):

        proto_rows = types.ProtoRows()
        for row in chunk:
            row_count += 1
            proto_rows.serialized_rows.append(row.SerializeToString())

        # Create an append row request containing the rows
        request = types.AppendRowsRequest()
        proto_data = types.AppendRowsRequest.ProtoData()
        proto_data.rows = proto_rows
        request.proto_rows = proto_data

        future = append_rows_stream.send(request)

        response_futures.append(future)

    # Wait for all the append row requests to finish.
    for f in response_futures:
        f.result()

    # Shutdown background threads and close the streaming connection.
    append_rows_stream.close()

    return row_count


def create_row_bme280(beehiveid: str, sensorid: str, temperature_f:float, humidity_prcnt:float, barometricpressure_hpa:float):
    row = bme280_pb2.BME280()
    row.timestamp = time.time_ns() // 1_000_000 # Time in milliseconds after epoch
    row.beehiveid = beehiveid
    row.sensorid = sensorid
    row.temperature_f = temperature_f
    row.humidity_prcnt = humidity_prcnt
    row.barometricpressure_hpa = barometricpressure_hpa
    time.sleep(0.01)
    return row


def main():

    write_client = bigquery_storage_v1.BigQueryWriteClient()

    rows = [ 
        create_row_bme280('TestHive', '1', i+32., i+50., i+1000.) 
        for i in range(0,20)  
    ]

    send_rows_to_bq("smart-beehive-431213", "sensor_data", "bme280", write_client, rows)

if __name__ == '__main__':
    main()