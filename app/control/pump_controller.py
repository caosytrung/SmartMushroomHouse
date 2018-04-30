import threading
import json
from app.model.pump_control_data import PumbControlData
from app.config.mqtt_config import *
import  RPi.GPIO as GPIO
import time
from enum import Enum



ON_COMMAND ="ON"
OFF_COMMAND ="OFF"
DELAY_COMMAND ="DELAY"
pins = [18,17,15,14]
GPIO.setup(pins, GPIO.OUT)

class PumpController(threading.Thread):
    def __init__(self):
        for pin in pins:
            time.sleep(1/10)
            GPIO.output(pin,GPIO.HIGH)
        self.isDelay = False
        self.state = OFF_COMMAND


    def run(self):
        self.processData()

    def turnPumpOn(self):
        if(self.state == OFF_COMMAND):
            self.isDelay = True
            GPIO.output(self.pumpControl.relayId,GPIO.LOW)
            self.state = ON_COMMAND

    def turnPumpOff(self):
        if(self.state == ON_COMMAND):
            GPIO.output(self.pumpControl.relayId, GPIO.HIGH)
            self.state = OFF_COMMAND

    def processData(self):

        while 1:
            controlData = self.pumpControl
            if controlData is None:
                time.sleep(1)
                continue

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
                if(self.isDelay):
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
