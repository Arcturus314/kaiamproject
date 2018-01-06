#Kaveh Pezeshki
#Dec 16 2017
#Python driver for the LSM303 Magnetometer on I2C


#The Adafruit LSM303 package must be installed for this script to function. It is available at:
#   https://github.com/adafruit/Adafruit_Python_LSM303

#Data is returned after offset and scale adjustment, via the formula:
#   output = raw*scale - offset

import Adafruit_LSM303

#status tracks whether the last tested isolator is in spec
status = "INIT FAILED"

#x, y, and z offsets- set by the program during calibration
offsets = [0,0,0]

#x, y, and z scale- these are set by the user
#these values are currently set to the +/-1.3 Gauss FSD LSB/mgauss setting in the LSM303 datasheet:
#   http://www.st.com/content/ccc/resource/technical/document/datasheet/56/ec/ac/de/28/21/4d/48/DM00027543.pdf/files/DM00027543.pdf/jcr:content/translations/en.DM00027543.pdf
#   X/Y: 1100 LSB/Gauss
#   Z  : 980  LSB/Gauss
scale   = [0.9091,0.9091,1.0204]

#acceptable magnetic field strength ranges in mgauss- FOR TEMPORARY METRIC
X_RANGE = [-1000,1000]
Y_RANGE = [-1000,1000]
Z_RANGE = [-1000,1000]


def calc_status(mag):
    '''calculates whether the tested isolator is in spec
    THIS FUNCTION WILL NEED TO BE MODIFIED'''

    #as this method modifies status
    global status

    #no assignment is done if there is a sensor failure
    if status == "INIT FAILED": return
    mag_x, mag_y, mag_z = mag

    #THIS WILL NEED TO BE MODIFIED
    #The current metric tests whether the X, Y, and Z-axis magnetic field strength values are within the bounds of X_RANGE, Y_RANGE, and Z_RANGE.
    #   These bounds are set at +/- 1 Gauss- this was an arbitrary value, and will need to be adjusted depending on the isolator.
    if mag_x <= X_RANGE[0] or mag_x >= X_RANGE[1] or mag_y <= Y_RANGE[0] or mag_y >= Y_RANGE[1] or mag_z <= Z_RANGE[0] or mag_z >= Z_RANGE[1]:
        status = "TEST FAILED"
    else: status = "TEST PASSED"

def setup_magnetometer():
    '''Initializes communication with the magnetometer and sets sensor parameters'''

    #setting global variables
    global status

    #setting global parameters
    global lsm303
    global status

    #the Adafruit script will fail in the case of I2C error
    try:
        lsm303=Adafruit_LSM303.LSM303()
        status = "NO DATA"
    except:
        status = "INIT FAILED"
    return

def read_magnetometer():
    '''reads the magnetometer, returning a tuple of x,y, and z values adjusted by scale and offsets'''

    #setting global variables
    global status

    #(0,0,0) is returned if there is a sensor or communication failure
    if status == "INIT FAILED": return (0,0,0)
    try:
        accel, mag = lsm303.read()
        #calculation of adjusted values
        return (mag[0]*scale[0]-offsets[0], mag[1]*scale[1]-offsets[1], mag[2]*scale[2]-offsets[2])
    except:
        status = "INIT FAILED"
        return (0,0,0)

def calibrate():
    '''calibrates the magnetometer to the current set of values by assigning magnetometer values to offsets'''

    #declared as global as offsets are modified
    global offsets
    global status

    #no calibration is done if there is a sensor failure
    if status == "INIT FAILED": return
    try:
        accel, mag = lsm303.read()
        #assigning offsets to be read magnetometer values
        offsets = (mag[0]*scale[0], mag[1]*scale[1], mag[2]*scale[2])
    except:
        status = "INIT FAILED"

def get_status():
    '''returns the result of the most recent magnetometer test'''
    return status

def get_offsets():
    '''returns the current offsets'''
    return offsets

