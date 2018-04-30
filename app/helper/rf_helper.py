from app.rf_lib.RF import NRF24
from app.config.rf_data_config import *
import time
import RPi.GPIO as GPIO
import spidev

class RfHelper:
    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.NRF24 = NRF24(GPIO, spidev.SpiDev())

    '''
        Startup config for RF receiver mode
    '''
    def setup(self):
        self.NRF24.begin(0, 25)
        self.NRF24.setPayloadSize(RF_PLAYLOAD_SIZE)
        self.NRF24.setChannel(RF_CHANNEL)
        self.NRF24.setDataRate(NRF24.BR_1MBPS)
        self.NRF24.setPALevel(NRF24.PA_MIN)

        self.NRF24.setAutoAck(True)
        self.NRF24.enableDynamicPayloads()
        self.NRF24.enableAckPayload()

        self.NRF24.openReadingPipe(1, PIPES[1])
        self.NRF24.openReadingPipe(0, PIPES[0])
        self.NRF24.openReadingPipe(2, PIPES[2])
        self.NRF24.printDetails()

    def startListeningData(self):
        self.NRF24.startListening()

    def readDataintoByteArray(self):
        recvMes = []
        while not self.NRF24.available([0]):
            time.sleep(1 / 100)
        time.sleep(1/10)
        recvMes = []
        self.NRF24.read(recvMes, self.NRF24.getDynamicPayloadSize())
        return  recvMes