

CLUSTER_INDEX = 0
FARM_ID = 1

'''
Temperature data
'''
TEMP_EXISTS_INDEX = 1
TEMP_INT_INDEX = 2
TEMP_FRACTION_INDEX = 3

'''
Hummidity data
'''
HUMI_EXISTS_INDEX = 4
HUMI_INT_INDEX = 5
HUMI_FRACTION_INDEX = 6

'''
Co2 data
'''
CO2_EXISTS_INDEX = 7
CO2_INT_INDEX = 8
CO2_FRACTION_INDEX = 9

'''
illuminance data
'''
ILLUMINANCE_EXISTS_INDEX = 10
ILLUMINANCE_INT_INDEX = 11
ILLUMINANCE_FRACTION_INDEX = 12

''''
pipes address for receiver data
'''
PIPES = [[0xF0, 0xF0, 0xF0, 0xF0, 0xE2], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1],
         [0xF0, 0xF0, 0xF0, 0xF0, 0xE3]]
RF_PLAYLOAD_SIZE = 32
RF_CHANNEL = 0x76