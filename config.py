import os

SAMPLE_TIME=os.getenv("SAMPLE_TIME", default = 30) # sample time in seconds to retrieve data from battery

BATTERY_IP=os.getenv("BATTERY_IP", default = "192.168.1.1")

DB_HOST=os.getenv("DB_HOST", default = "postgres")
DB_NAME=os.getenv("DB_NAME", default = "pv")
DB_USER=os.getenv("DB_USER", default = "user")
DB_PWD=os.getenv("DB_PWD", default = "password")

CSV_FILE=os.getenv("CSV_FILE", default = "data.csv")
