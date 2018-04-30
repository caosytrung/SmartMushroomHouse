from app.config.mqtt_config import *
from app.config.rf_data_config import *

class SensorData:
    def __init__(self,clusterId,farmId,temp,humi,co2,illum,timestamp):
        self.clusterId = clusterId
        self.farmId = farmId
        self.temp = temp
        self.humi = humi
        self.co2 = co2
        self.illum = illum
        self.timestamp = timestamp

    def objectToJson(self):
        data = {JSON_CLUSTER_ID_KEY:str(self.clusterId),
                JSON_FARM_ID_KEY: str(self.farmId),
                JSON_TEMP_KEY: self.temp,
                JSON_HUMP_KEY: self.humi,
                JSON_CO2_KEY: self.co2,
                JSON_ILLU_KEY: self.illum
                }

        return  data