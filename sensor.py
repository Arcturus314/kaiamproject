#Kaveh Pezeshki
#Dec 16 2017
#Python driver for the LSM303 Magnetometer on I2C

import random
import Adafruit_LSM303

X_RANGE = [-1000,1000]
Y_RANGE = [-1000,1000]
Z_RANGE = [-1000,1000]

#0.75, 1.5, 3.0, 7.5, 15, 30, or 75 Hz
OUTPUT_RATE = 30

#NORMAL, POS_BIAS, NEG_BIAS
OUTPUT_CONFIG = "NORMAL"

#1.3, 1.9, 2.5, 4.0, 4.7, 5.6, 8.1 Gauss
FSD = 4

ADDR = (0x3C >> 1)

status = "INIT FAILED"

#x, y, and z offsets
offsets = [0,0,0]


def setup_magnetometer(address = (0x3C >> 1)):
    #Initializes communication with the magnetometer and sets sensor parameters
    global lsm303
    global status
    try:
        lsm303=Adafruit_LSM303.LSM303()
        status = "NO DATA"
    except:
        status = "INIT FAILED"
    return

def read_magnetometer():
    #reads the magnetometer, returning a tuple of 
    if status == "INIT FAILED": return (0,0,0)
    accel, mag = lsm303.read()
    return (mag[0]-offsets[0], mag[1]-offsets[1], mag[2]-offsets[2])

def calibrate():
    global offsets
    if status == "INIT FAILED": return
    accel, mag = lsm303.read()
    offsets = mag

def calc_status(mag):
    #calculates whether the tested magnet is in range
    global status
    if status == "INIT FAILED": return
    mag_x, mag_y, mag_z = mag
    if mag_x <= X_RANGE[0] or mag_x >= X_RANGE[1] or mag_y <= Y_RANGE[0] or mag_y >= Y_RANGE[1] or mag_z <= Z_RANGE[0] or mag_z >= Z_RANGE[1]:
        status = "FAILED"
    else: status = "PASSED"

def get_status():
    #returns the status of the magnetometer testing
    return status

