import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pipes = [[0xF0, 0xF0, 0xF0, 0xF0, 0xE2], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1],
         [0xF0, 0xF0, 0xF0, 0xF0, 0xE3]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0,25)
radio.setPayloadSize(32)
radio.setChannel(0x76)

radio.setDataRate(NRF24.BR_1MBPS)

#radio.setPALevel(NRF24.PA_MIN)
#radio.setAutoAck(True)
#radio.enableDynamicPayloads()

radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1,pipes[1])
radio.openReadingPipe(0,pipes[0])
radio.openReadingPipe(2,pipes[2])
radio.printDetails()

radio.startListening()
print("Starting    ..")
count = 0
while(1):
    
    start = time.time()
   
    while not radio.available([0]):
        time.sleep(1 / 100)
       
    recvMes = []
    radio.read(recvMes,radio.getDynamicPayloadSize())
    print("Received : {}".format(recvMes))
    
    print("Translating the recvMes into unicode characters ..")

    string = ""

    for n in recvMes :
      if(n >=32 and n<= 126):
          string += chr(n)
    print(string)
    count = count +1
    print("Count Value : ")
    print(count)
