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

  logging.basicConfig(level=logging.INFO)

  signal.signal(signal.SIGINT, signal_handler)

  sonnen_batterie = Battery(config.BATTERY_IP)  

  db_conn = None
  try:
    db_conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (config.DB_NAME, config.DB_USER, config.DB_HOST, config.DB_PWD))
    logging.info("Successfully connected to PostgreSQL database %s@%s!" % (config.DB_NAME, config.DB_HOST))
  except:
    logging.warning("Unable to connect to the database")

  csv_fp = None
  try:
    csv_fp = open(config.CSV_FILE, "w+")
    csv_fp.write("production_w, consumption_w, grid_feed_in_w, grid_retrieve_w, battery_level, battery_charge_w, battery_discharge_w, consumption_ws, production_ws, grid_feed_in_ws, grid_retrieve_ws, battery_charge_ws, battery_discharge_ws\n")
  except:
    logging.warning("Unable to open %s." % config.CSV_FILE)
    
  while(True):
    sonnen_batterie.update_data()
    data = sonnen_batterie.get_last_valid_data()
    if db_conn:
      # check connection by executing a simple query
      try:
        cursor = db_conn.cursor()
	cursor.execute('SELECT VERSION()')
	row = cursor.fetchone()
      except Exception as ex:
        logging.error("%s" % repr(ex))	
        logging.error("Connection to database seems to be broken! re-connectiong...!")
        db_conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (config.DB_NAME, config.DB_USER, config.DB_HOST, config.DB_PWD))
        logging.info("Successfully connected to PostgreSQL database %s@%s!" % (config.DB_NAME, config.DB_HOST))
      db_conn.cursor().execute("INSERT INTO measurements( \
	                          production_w, consumption_w, grid_feed_in_w, grid_retrieve_w, battery_level, \
				  battery_charge_w, battery_discharge_w, consumption_ws, production_ws, grid_feed_in_ws, \
                                  grid_retrieve_ws, battery_charge_ws, battery_discharge_ws) \
	                          VALUES (%i, %i, %i, %i, %i, %i, %i, %f, %f, %f, %f, %f, %f);" % 
                            (data.get_production_w(),        data.get_consumption_w(), 
			     data.get_grid_feed_in_w(),       data.get_grid_retrieve_w(),     data.get_battery_level(),
			     data.get_battery_charge_w(),     data.get_battery_discharge_w(), data.get_energy_consumption_ws(),
			     data.get_energy_production_ws(), data.get_energy_feed_in_ws(),   data.get_energy_retrieved_ws(),
                             data.get_battery_charge_ws(), data.get_battery_discharge_ws()))

      db_conn.commit()
    
    if csv_fp:
      csv_fp.write("%s,%i,%i,%i,%i,%i,%i,%i,%f,%f,%f,%f,%f,%f\n" % 
                            (data.get_timestamp(),            data.get_production_w(),        data.get_consumption_w(), 
			     data.get_grid_feed_in_w(),       data.get_grid_retrieve_w(),     data.get_battery_level(),
			     data.get_battery_charge_w(),     data.get_battery_discharge_w(), data.get_energy_consumption_ws(),
			     data.get_energy_production_ws(), data.get_energy_feed_in_ws(),   data.get_energy_retrieved_ws(),
                             data.get_battery_charge_ws(), data.get_battery_discharge_ws()))
		   
    if not db_conn and not csv_fp:
      logging.debug(data) 
    time.sleep(config.SAMPLE_TIME)
  
  
