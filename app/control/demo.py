
import json
import time
from app.helper.rf_helper import RfHelper
from app.helper.mqtt_client_helper import  MqttClientHelper
from app.config.mqtt_config import SENSOR_DATA_TOPIC,PUMP_CONTROLLER_TOPIC
from  pump_controller import  PumpController
from  app.model.pump_control_data import PumbControlData
from app.config.mqtt_config import *
from  app.config.rf_data_config import  *
from app.decrypt.AES_decrypt import AesDecryptData

def on_message(client, userdata, msg):

    if(str(msg.topic) == PUMP_CONTROLLER_TOPIC):
        print("PUMP CONTROLLER")
        print(str(msg.payload))
        jsonData = str(msg.payload)
        jsonArr = json.loads(jsonData)
        pumpControl = PumbControlData(jsonArr[JSON_CLUSTER_ID_KEY],
                                      jsonArr[JSON_COMMAND],
                                      jsonArr[JSON_DURATION],
                                      jsonArr[JSON_OFF_DURATION])
        relayId =  CLUSTER_RELAY_MAPPING.get(pumpControl.clusterId)
        if(relayId == 18):
            pumpControlCluster0.readJsonData(jsonData)
        elif(relayId == 14):
            pumpControlCluster2.readJsonData(jsonData)
def on_message1(client, userdata, msg):

    if(str(msg.topic) != SENSOR_DATA_TOPIC):
        print ("DICFFERENT TOPIC")
       


# sensor data mqtt-------------

sensorMqttHelper = MqttClientHelper()
sensorMqttHelper.setup()
sensorMqttHelper.setTopic(SENSOR_DATA_TOPIC)
sensorMqttHelper.setMessageListerner(on_message1)
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
pumpControlCluster0 = PumpController(18)
pumpControlCluster0.start()

pumpControlCluster2 = PumpController(14)
pumpControlCluster2.start()
# Decrypt
decryptData = AesDecryptData();


print("Starting    ..")

while True:

    recvMes = rfHelper.readDataintoByteArray()
    decryptData.setCipherData(recvMes)
    plainData = decryptData.decryptData()
    print("Transmit : {}".format(plainData))
    jsonData = sensorMqttHelper.publishDataToBroker(plainData)
    #print(jsonData)
    time.sleep(1)


