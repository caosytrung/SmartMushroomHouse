import RPi.GPIO as GPIO
from app.rf_lib.RF import NRF24
import time
import spidev
import paho.mqtt.client as mqtt
import json
from datetime import datetime

checkk = False

CLUSTER_INDEX = 0;
FARM_ID = 1;
TEMP_EXISTS_INDEX = 1;
TEMP_INT_INDEX = 2;
TEMP_FRACTION_INDEX = 3;

HUMI_EXISTS_INDEX = 4;
HUMI_INT_INDEX = 5;
HUMI_FRACTION_INDEX = 6;

CO2_EXISTS_INDEX = 7;
CO2_INT_INDEX = 8;
CO2_FRACTION_INDEX = 9;

ILLUMINANCE_EXISTS_INDEX = 10;
ILLUMINANCE_INT_INDEX = 11;
ILLUMINANCE_FRACTION_INDEX = 12;


def on_connect(client, userdata, flags, rc):
    print('Connected with result code ', rc)
    if rc == 0:
        checkk = True
        print("Connected Ok")
    else:
        print("Bad Connection")
    client.subscribe('sensor_data')


def on_message(client, userdata, msg):
    print("" + msg.topic + " " + str(msg.payload))
    print("\n")


# mqtt-------------

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set('vgomwcel', 'u8tzlVTr_da2')
client.connect('m14.cloudmqtt.com', 13894, 60)
client.loop_start()

# mqtt-------------


GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pipes = [[0xF0, 0xF0, 0xF0, 0xF0, 0xE2], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1],
         [0xF0, 0xF0, 0xF0, 0xF0, 0xE3]]

radio = RF.NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 25)
radio.setPayloadSize(32)
radio.setChannel(0x76)

radio.setDataRate(NRF24.BR_1MBPS)

# radio.setPALevel(NRF24.PA_MIN)
# radio.setAutoAck(True)
# radio.enableDynamicPayloads()

radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipes[1])
radio.openReadingPipe(0, pipes[0])
radio.openReadingPipe(2, pipes[2])
radio.printDetails()

radio.startListening()
print("Starting    ..")
count = 0
while True:
    # ackPL =[1]
    start = time.time()
    # while not radio.available():
    #    time.sleep(1 / 100)
    #    if time.time() - start > 3:
    #        print("Timed out.")
    #        break

    # ackPL =[1]
    while not radio.available([0]):
        time.sleep(1 / 100)
    time.sleep(1)
    recvMes = []
    radio.read(recvMes, radio.getDynamicPayloadSize())
    print("Received : {}".format(recvMes))

    clusterID = recvMes[CLUSTER_INDEX]
    temp = 0;
    humi = 0;
    co2 = 0;
    illu = 0;
    if (recvMes[TEMP_EXISTS_INDEX] == 1):
        temp = recvMes[TEMP_INT_INDEX] + recvMes[TEMP_FRACTION_INDEX] * 1.0 / 100
    if (recvMes[HUMI_EXISTS_INDEX] == 1):
        humi = recvMes[HUMI_INT_INDEX] + recvMes[HUMI_FRACTION_INDEX] * 1.0 / 100
    if (recvMes[CO2_EXISTS_INDEX] == 1):
        co2 = recvMes[CO2_INT_INDEX] + recvMes[CO2_FRACTION_INDEX] * 1.0 / 100
    if (recvMes[ILLUMINANCE_EXISTS_INDEX] == 1):
        illu = recvMes[ILLUMINANCE_INT_INDEX] + recvMes[ILLUMINANCE_FRACTION_INDEX] * 1.0 / 100

    print("Datas From sensor : {} . {}".format(temp, humi))

    if 1 > 0:
        dt = datetime.now()

        data = {'cluster_id': str(clusterID),
                'farm_id': str(FARM_ID),
                'temperature': temp,
                'humidity': humi,
                'co2': co2,
                'illuminance': illu}
        client.publish('sensor_data', json.dumps(data), 0, True)
        print(checkk)
        print('Sending value: ' % data + "aaa")
        time.sleep(1)
    else:
        print('Fall Sending value: ')
    # radio.writeAckPayload(1,ackPL,len(ackPL))
# print("Loaded payload {}".format(ackPL))

