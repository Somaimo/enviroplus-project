# Example IoT Project - With Pimoroni enviro+

## Introduction

This repository holds an example script to display the sensor data from a Pimoroni enviro+ HAT. This is not a production ready script and only really here as a proof of concept.

Additionally there is an example function implementation to send data to a InfluxDB instance. It is configured to send the data to influxdb.phys.ethz.ch.

IMPORTANT

You need to change the username, password, database variables inside [influxdata.py](./influxdata.py) file. Without it the script will fail!

## Requirements

You need the following things for this to work:

- Enviro+ Library - <https://learn.pimoroni.com/article/getting-started-with-enviro-plus>
-- run the install-bullseye.sh script

## Additional Information

The additional file `sensordata.service` can be used to enable the script as a service. If you want to use it, you have to change the path to the script.

## DISCLAIMER

As mentioned in the beginnging. The content in this directory is not meant to be production ready and should not be copied 1:1. It is only here to illustrate how it could work.

## Copyright

This was made for ETH Zürich by Marc Winkler.
