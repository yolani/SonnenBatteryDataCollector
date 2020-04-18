import os

SAMPLE_TIME=int(os.getenv("SAMPLE_TIME", default = 30)) # sample time in seconds to retrieve data from battery

BATTERY_IP=os.getenv("BATTERY_IP", default = "192.168.1.106")

DB_HOST=os.getenv("DB_HOST", default = "192.168.1.123")
DB_NAME=os.getenv("DB_NAME", default = "pv")
DB_USER=os.getenv("DB_USER", default = "pv_user")
DB_PWD=os.getenv("DB_PWD", default = "pv_password")

CSV_FILE=os.getenv("CSV_FILE", default = "data.csv")
