import paho.mqtt.client as mqtt
from app.config.mqtt_config import *
from app.config.rf_data_config import *
from app.model.sensor_data import SensorData
import json

class MqttClientHelper:
    def __init__(self):
        self.mqttClient = mqtt.Client()

    def setup(self):
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.on_message = self.on_message
        self.mqttClient.username_pw_set(MQTT_CLIENT_USERNAME, MQTT_CLIENT_PASSWORD)
        self.mqttClient.connect(MQTT_HOST, MQTT_PORT, 60)
        self.mqttClient.loop_start()

    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print("Connected Ok")
            client.subscribe('sensor_data')
        else:
            print("Bad Connection")

    def on_message(self,client, userdata, msg):
        print("" + msg.topic + " " + str(msg.payload))
        print("\n")

    def startLoop(self):
        self.mqttClient.loop_start()

    def publishDataToBroker(self,recvMes):
        sensorData = SensorData()

        sensorData.clusterId = recvMes[CLUSTER_INDEX]
        sensorData.farmId = FARM_ID;
        if (recvMes[TEMP_EXISTS_INDEX] == 1):
            sensorData.temp = recvMes[TEMP_INT_INDEX] + recvMes[TEMP_FRACTION_INDEX] * 1.0 / 100
        if (recvMes[HUMI_EXISTS_INDEX] == 1):
            sensorData.humi = recvMes[HUMI_INT_INDEX] + recvMes[HUMI_FRACTION_INDEX] * 1.0 / 100
        if (recvMes[CO2_EXISTS_INDEX] == 1):
            sensorData.co2 = recvMes[CO2_INT_INDEX] + recvMes[CO2_FRACTION_INDEX] * 1.0 / 100
        if (recvMes[ILLUMINANCE_EXISTS_INDEX] == 1):
            sensorData.illum = recvMes[ILLUMINANCE_INT_INDEX] + recvMes[ILLUMINANCE_FRACTION_INDEX] * 1.0 / 100

        jsonData = sensorData.objectToJson()
        self.mqttClient.publish(SENSOR_DATA_TOPIC, json.dumps(jsonData), 0, True)

        return jsonData