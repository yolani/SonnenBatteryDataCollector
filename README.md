# SonnenBatteryDataCollector
Python-Script that collects data from „Sonnen-Batterie“ through the REST-API and pushes it to different data storages.

# Usage

## Configuration
Currentely done through environment variables:
- SAMPLE_TIME: Interval in which the battery shall be queried in seconds
- BATTERY_IP: IP-address / hostname of the battery
- DB_HOST: Hostname / IP-address of the PostgreSQL database
- DB_NAME: database name of the PostgreSQL database
- DB_USER:User for the PostgreSQL database
- DB_PWD: Password of DB_USER
- CSV_FILE: Path to write the data in CSV format to

## Run it

- Either directely as a Python-Script: "python3 main.py"
- As a docker image: "docker run -d yolani/sbdc[:latest]"

## Output

- Data is pushed to PostgreSQL database if provided connection details are valid (can be used additionally to csv output)
- Data is written / appended to CSV file if provided file path can be written (can be used additionally to database output)
- Data is written to stdout if neither database nor CSV file are available
