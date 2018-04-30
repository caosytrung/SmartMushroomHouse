from app.config.mqtt_config import *
from app.config.rf_data_config import *

class SensorData:
    def __init__(self):
        self.clusterId = "0"
        self.farmId = "0"
        self.temp = 0
        self.humi = 0
        self.co2 = 0
        self.illum = 0
        self.timestamp = 0

    def objectToJson(self):
        data = {JSON_CLUSTER_ID_KEY:str(self.clusterId),
                JSON_FARM_ID_KEY: str(self.farmId),
                JSON_TEMP_KEY: self.temp,
                JSON_HUMP_KEY: self.humi,
                JSON_CO2_KEY: self.co2,
                JSON_ILLU_KEY: self.illum,
                JSON_TIMESTAMP_KEY: self.timestamp
                }

        return  data