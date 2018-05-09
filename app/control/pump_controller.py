import threading
import json
from app.model.pump_control_data import PumbControlData
from app.config.mqtt_config import *

import time
import RPi.GPIO as GPIO

ON_COMMAND ="ON"
OFF_COMMAND ="OFF"
DELAY_COMMAND ="DELAY"


class PumpController(threading.Thread):
    def __init__(self,relayID):
        super(PumpController, self).__init__()
        self.pins = relayID
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pins, GPIO.OUT)
        GPIO.output(self.pins, GPIO.HIGH)
        self.isDelay = False
        self.state = OFF_COMMAND


    def run(self):
        self.processData()

    def turnPumpOn(self):
        if(self.state == OFF_COMMAND):
            print("TURNNNNNNNN On Pin {0}".format(self.pumpControl.relayId))
            self.isDelay = True
            GPIO.output(int(self.pumpControl.relayId),GPIO.LOW)
            self.state = ON_COMMAND

    def turnPumpOff(self):
        if(self.state == ON_COMMAND):
            GPIO.output(int(self.pumpControl.relayId), GPIO.HIGH)
            self.state = OFF_COMMAND

    def processData(self):

        while 1:
            if  not hasattr(self,'pumpControl'):
                time.sleep(1)
                continue
            controlData = self.pumpControl
            print("VAOXONOOOAAAAA") 
            if(self.isDelay and self.pumpControl.offDuration > 0):
                self.pumpControl.offDuration -= 1
            elif (self.isDelay and self.pumpControl.offDuration <=0):
                self.isDelay = False

            if (controlData.command == OFF_COMMAND and controlData.duration > 0):
                self.turnPumpOff()
                self.pumpControl.duration = 0

            elif(self.pumpControl.duration <= 0 and
                 self.pumpControl.command == ON_COMMAND):
                self.turnPumpOff()

            elif(self.pumpControl.duration > 0 and
                 self.pumpControl.command == ON_COMMAND):
                self.pumpControl.duration -= 1
                if(not self.isDelay):
                    self.turnPumpOn()
            else:
                self.turnPumpOff()


            time.sleep(1)

    def readJsonData(self, jsonData):
        jsonArr = json.loads(jsonData)
        if(self.isDelay and jsonArr[JSON_COMMAND] == ON_COMMAND):
            return
        self.pumpControl = PumbControlData(jsonArr[JSON_RELAY_ID],
                                      jsonArr[JSON_COMMAND],
                                      jsonArr[JSON_DURATION],
                                      jsonArr[JSON_OFF_DURATION])

