import logging
import psycopg2
import signal
import time
import sys

from battery import Battery
import config

def cleanup():
  # TODO: Future use, close database connection, final commit, etc.
  pass

def signal_handler(sig, frame):
    logging.info("shutting down...")
    signal.signal(sig, signal.SIG_IGN)
    cleanup()
    sys.exit(0)

if __name__ == "__main__":

  signal.signal(signal.SIGINT, signal_handler)

  sonnen_batterie = Battery("192.168.1.106", store_fcts=[print, ])  

  db_conn = None
  try:
    db_conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (config.DB_NAME, config.DB_USER, config.DB_HOST, config.DB_PWD))
  except:
    logging.warning("Unable to connect to the database")

  csv_fp = None
  try:
    csv_fp = open(config.CSV_FILE, "w+")
  except:
    logging.warning("Unable to open %s." % config.CSV_FILE)

    
  while(True):
    sonnen_batterie.update_data()
    data = sonnen_batterie.get_last_valid_data()
    if db_conn:
      db_conn.cursor().execute("INSERT INTO measurements( \
	                          \"timestamp\", production_w, consumption_w, grid_feed_in_w, grid_retrieve_w, battery_level, \                            battery_charge_w, battery_discharge_w, consumption_ws, production_ws, grid_feed_in_ws, \
                            grid_retrieve_ws, battery_charge_ws, battery_discharge_ws) \
	                          VALUES ('%s'::timestamptz, %i, %i, %i, %i, %i, %i, %i, %f, %f, %f, %f, %f, %f);" % 
                            (data.get_timestamp(),
                             data.get_production_w(), data.get_consumption_w(), data.get_grid_feed_in_w(),
                             data.get_grid_retrieve_w(), data.get_battery_level(), data.get_battery_charge_w(),
                             data.get_battery_discharge_w(), data.get_energy_consumption_ws(), data.get_energy_production_ws(),
                             data.get_energy_feed_in_ws(), data.get_energy_retrieved_ws(),
                             data.get_battery_charge_ws(), data.get_battery_discharge_ws()))
      db_conn.commit()
    
    if csv_fp:
      csv_fp.write("Bla")
    if not db_conn and not csv_fp:
      print(data) 
    time.sleep(config.SAMPLE_TIME)
  
  
