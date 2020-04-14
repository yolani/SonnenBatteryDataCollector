import datetime
import json
import logging
import numpy
import pytz
import requests
import time
import tzlocal

class BatteryData():
  def __init__(self, json_data, last_data=None):
    '''
    {
      "Apparent_output":3105,
      "BackupBuffer":"0",
      "BatteryCharging":false,
      "BatteryDischarging":true,
      "Consumption_W":3914,
      "Fac":50,
      "FlowConsumptionBattery":true,
      "FlowConsumptionGrid":true,
      "FlowConsumptionProduction":true,
      "FlowGridBattery":false,
      "FlowProductionBattery":false,
      "FlowProductionGrid":false,
      "GridFeedIn_W":-30,
      "IsSystemInstalled":1,
      "OperatingMode":"2",
      "Pac_total_W":3073,
      "Production_W":792,
      "RSOC":99,
      "Sac1":1022,
      "Sac2":1036,
      "Sac3":1047,
      "SystemStatus":"OnGrid",
      "Timestamp":"2020-04-09 19:04:42",
      "USOC":99,
      "Uac":240,
      "Ubat":48,
      "dischargeNotAllowed":false,
      "generator_autostart":false}
    '''
    
    # create real timestamp from battery info and add timezone information for correct representation later on
    self.__timestamp = get_localzone().localize(datetime.datetime.timestamp(datetime.datetime.strptime(json_data["Timestamp"], "%Y-%m-%d %H:%M:%S")))
    # self.__timestamp = datetime.datetime.timestamp(datetime.datetime.strptime(json_data["Timestamp"], "%Y-%m-%d %H:%M:%S"))

    self.__production = int(json_data["Production_W"])
    self.__consumption = int(json_data["Consumption_W"])
    self.__grid_feed_in = max(int(json_data["GridFeedIn_W"]), 0)
    self.__grid_retrieve = abs(min(int(json_data["GridFeedIn_W"]), 0))
    self.__battery_charge_level = int(json_data["USOC"])
    self.__battery_discharge = max(int(json_data["Pac_total_W"]), 0)
    self.__battery_charge = abs(min(int(json_data["Pac_total_W"]), 0))
    self.__energy_consumed = 0
    self.__energy_produced = 0
    self.__energy_ingested = 0
    self.__energy_retrieved = 0
    self.__energy_charge = 0
    self.__energy_discharge = 0

    if last_data:
      time_diff_s = self.get_timestamp() - last_data.get_timestamp()
      self.__energy_consumed = numpy.trapz(numpy.array([last_data.get_consumption_w(), self.get_consumption_w()]), dx = time_diff_s)
      self.__energy_produced = numpy.trapz(numpy.array([last_data.get_production_w(), self.get_production_w()]), dx = time_diff_s)
      self.__energy_ingested = numpy.trapz(numpy.array([last_data.get_grid_feed_in_w(), self.get_grid_feed_in_w()]), dx = time_diff_s)
      self.__energy_retrieved = numpy.trapz(numpy.array([last_data.get_grid_retrieve_w(), self.get_grid_retrieve_w()]), dx = time_diff_s)
      self.__energy_charge = numpy.trapz(numpy.array([last_data.get_battery_charge_w(), self.get_battery_charge_w()]), dx = time_diff_s)
      self.__energy_discharge = numpy.trapz(numpy.array([last_data.get_battery_discharge_w(), self.get_battery_discharge_w()]), dx = time_diff_s)
  
  def __repr__(self):
    return("%s | Akku-Ladestand: %02i%% | Produktion: %04i W | Verbrauch: %04i W | Einspeisung: %04i W | Netz-Bezug: %04i W"
    % (self.__timestamp, self.__battery_charge_level, self.__production, self.__consumption, self.__grid_feed_in, self.__grid_retrieve))

  def get_timestamp(self):
    return self.__timestamp

  def get_production_w(self):
    return self.__production

  def get_consumption_w(self):
    return self.__consumption

  def get_energy_consumption_ws(self):
    return self.__energy_consumed

  def get_energy_production_ws(self):
    return self.__energy_produced

  def get_energy_feed_in_ws(self):
    return self.__energy_ingested

  def get_energy_retrieved_ws(self):
    return self.__energy_retrieved

  def get_grid_feed_in_w(self):
    return self.__grid_feed_in

  def get_grid_retrieve_w(self):
    return self.__grid_retrieve

  def get_battery_level(self):
    return self.__battery_charge_level

  def get_battery_charge_w(self):
    return self.__battery_charge

  def get_battery_charge_ws(self):
    return self.__energy_charge

  def get_battery_discharge_w(self):
    return self.__battery_discharge

  def get_battery_discharge_ws(self):
    return self.__energy_discharge

class Battery():
  def __init__(self, ip_addr, store_fcts=None):
    self.__battery_ip = ip_addr
    self.__current_data = None
    self.__last_valid_data = None
    self.__output_fcts = store_fcts

  def update_data(self):
    response = requests.get('http://%s/api/v1/status' % self.__battery_ip)
    if response.status_code == 200:
      self.__current_data = BatteryData(json.loads(response.text), last_data=self.__current_data)
      self.__last_valid_data = self.__current_data
    else:
      self.__current_data = None

  def get_current_data(self):
    return self.__current_data

  def get_last_valid_data(self):
    return (self.__current_data if self.__current_data else self.__last_valid_data)
