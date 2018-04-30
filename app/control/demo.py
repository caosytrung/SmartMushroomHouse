
import json
import time
from app.helper.rf_helper import RfHelper
from app.helper.mqtt_client_helper import  MqttClientHelper
from app.config.mqtt_config import SENSOR_DATA_TOPIC,PUMP_CONTROLLER_TOPIC
from  pump_controller import  PumpController


def on_message(client, userdata, msg):
    print("hihihihihhihi")
    if(msg.topic == PUMP_CONTROLLER_TOPIC):
        print("hahahaahaaaaaaaaaaaaaa")
        jsonData = str(msg.payload)
        pumpControl.readJsonData(jsonData)



# sensor data mqtt-------------

sensorMqttHelper = MqttClientHelper()
sensorMqttHelper.setup()
sensorMqttHelper.setTopic(SENSOR_DATA_TOPIC)
sensorMqttHelper.setMessageListerner(on_message)
sensorMqttHelper.startLoop()

# sensor data mqtt-------------

controlMqttHelper = MqttClientHelper()
controlMqttHelper.setup()
controlMqttHelper.setTopic(PUMP_CONTROLLER_TOPIC)
controlMqttHelper.setMessageListerner(on_message)
controlMqttHelper.startLoop()

# nrf24l01-------------

rfHelper = RfHelper()
rfHelper.setup()
rfHelper.startListeningData()

#Pump
pumpControl = PumpController()
pumpControl.start()

print("Starting    ..")

while True:

    recvMes = rfHelper.readDataintoByteArray()
    print("Received : {}".format(recvMes))
    jsonData = sensorMqttHelper.publishDataToBroker(recvMes)
    print(jsonData)
    time.sleep(1)


