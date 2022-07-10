#!/usr/bin/env python3

import influxdb
import logging

# The following variables need to be updated, to set the correct user, password and db.
# This information can be found in Bitwarden.
client = influxdb.InfluxDBClient(
    host='influxdb.phys.ethz.ch',
    port=443,
    username='[write username]',
    password='[write user password]',
    database='[test or production db]',
    ssl=True,
    verify_ssl=True
)

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

def send_data(data,apprentice: str,room: str,measurement: str):
    '''
    This function takes in three parameters (data, tags and measurement)
    and sends them to the InlfuxDB instance.

        Parameters:
            data (float): String with the data of the sensor (without unit)
            measurement (string): String with the name of the measurement type, example: temperature, pressure, humidity, gas
            apprentice (string): Name of Apprentice (to filter in Grafana)
            room (string): Name of the room the sensor is in (exampleFormat: hcp_g_38-2)
    '''
    assert (data is not None)
    assert (measurement is not None)
    assert (apprentice is not None)
    assert (room is not None)
    data = float(data)
    json_body = [
        {
             "measurement": measurement,
             "tags": {
                 "apprentice": apprentice,
                 "room"      : room
             },
             "fields": {
                 "value": data
              }
        }
    ]
    logging.info('Adding data point for measurement: {} with value: {} for apprentice: {}'.format(measurement,data,apprentice))
    client.write_points(json_body)
