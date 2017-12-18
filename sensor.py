#Kaveh Pezeshki
#Dec 16 2017
#Python driver for the LSM303 Magnetometer on I2C

import random

#0.75, 1.5, 3.0, 7.5, 15, 30, or 75 Hz
OUTPUT_RATE = 30

#NORMAL, POS_BIAS, NEG_BIAS
OUTPUT_CONFIG = "NORMAL"

#1.3, 1.9, 2.5, 4.0, 4.7, 5.6, 8.1 Gauss
FSD = 4

ADDR = (0x3C >> 1)

STATUS = "INIT FAILED"

def setup_magnetometer(address = (0x3C >> 1)):
    #Initializes communication with the magnetometer and sets sensor parameters
    return

def read_magnetometer():
    #reads the magnetometer, returning a tuple of 
    returnList = 3*[random.randrange(5000,8000)]
    return returnList

def get_status():
    #returns the status of the magnetometer testing
    returnList = ["FAILED", "PASSED", "WARNING", "INIT FAILED"]
    return random.choice(returnList)


