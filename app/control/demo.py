
from app.rf_lib.RF import NRF24
import time
from app.helper.rf_helper import RfHelper
from app.helper.mqtt_client_helper import  MqttClientHelper


# mqtt-------------


mqttClientHelper = MqttClientHelper()
mqttClientHelper.setup()
mqttClientHelper.startLoop()

# nrf24l01-------------

rfHelper = RfHelper()
rfHelper.setup()
rfHelper.startListeningData()

print("Starting    ..")

while True:

    recvMes = rfHelper.readDataintoByteArray()
    print("Received : {}".format(recvMes))

    jsonData = mqttClientHelper.publishDataToBroker(recvMes)
    print(jsonData)
    time.sleep(1)


