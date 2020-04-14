# SonnenBatteryDataCollector
Python-Script that collects data from „Sonnen-Batterie“ through the REST-API and pushes it to different data storages.

# Usage

## Configuration

## Run it

- Either directely as a Python-Script: "python3 main.py"
- As a docker image: "docker run -d yolani/sbdc[:latest]"

## Output

- Data is pushed to PostgreSQL database if provided connection details are valid (can be used additionally to csv output)
- Data is written / appended to CSV file if provided file path can be written (can be used additionally to database output)
- Data is written to stdout if neither database nor CSV file are available
