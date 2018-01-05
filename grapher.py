#Kaveh Pezeshki
#Dec 16 2017
#Graphing interface for isolator project with button support


#imports
from tkinter import *
import sensor
import time
import RPi.GPIO as GPIO
import math


#set the maximum number of digits in the output
DIGITS=5

#True if the device should calibrate on boot
CALONSTART=False

class Window(Frame):
    '''Tkinter window'''
    def __init__(self, master=None):
        '''Setting up tkinter window Window'''
        Frame.__init__(self,master)
        self.master=master

def setup_gpio():
    '''initializes Raspberry Pi GPIO and sets pins 23 and 24 as inputs'''
    #Pin 23: red calibration button
    #Pin 24: black test button
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def setup_ui():
    '''Adds UI elements to Window'''

    #declaring fields as global
    global root
    global teststat
    global xval_label
    global yval_label
    global zval_label
    global tot_label

    #setting up sensor
    sensor.setup_magnetometer()

    #setting up window parameters
    root = Tk()
    root.title("MagnetTest V0.1")
    root.attributes('-fullscreen', True)
    app = Window(root)

    #setting up textboxes

    #user instructions
    instr = Text(root, height=5, width=70)
    instr.tag_configure("center", justify="center", font=("Helvetica", 20))
    instr.insert("1.0","RED=CALIBRATE | BLACK=TEST")
    instr.tag_add("center", "1.0", "end")
    instr.pack()
    #testing status
    teststat = Text(root, height = 1, width=50, font=("Helvetica", 42))
    teststat.tag_configure("center", justify="center")
    teststat.insert("2.0","NO DATA")
    teststat.tag_add("center", "1.0", "end")
    teststat.pack()
    #sensor magnitude
    tot_label = Text(root, height = 1, width=50, font=("Helvetica", 30))
    tot_label.tag_configure("center", justify="center")
    tot_label.insert("2.0","Total Field Strength = 0.000 mgauss")
    tot_label.tag_add("center", "1.0", "end")
    tot_label.pack()
    #sensor values
    xval_label = Label(root, text="x=0.000 mg", font=("Helvetica",36))
    xval_label.pack(padx=5,pady=10,side=LEFT)
    yval_label = Label(root, text="y=0.000 mg", font=("Helvetica",36))
    yval_label.pack(padx=5,pady=10,side=LEFT)
    zval_label = Label(root, text="z=0.000 mg", font=("Helvetica",36))
    zval_label.pack(padx=5,pady=10,side=RIGHT)

    #updating Window
    root.update()

def sensortest():
    '''reads sensor data and updates Window fields, as well as calculating whether the tested isolator is in spec'''

    #reading the maggnetometer
    (xval, yval, zval) = sensor.read_magnetometer()
    sensor.calc_status((xval, yval, zval))
    sensor_status = sensor.get_status()

    #clearing the sensor status field
    teststat.delete("1.0","11.0")
    teststat.insert("1.0", sensor_status)

    #updating magnetic field strength measurements and Window
    update_magnetometer()

def update_magnetometer():
    '''reads sensor data and updates Window fields'''

    #reading magnetometer data
    (xval, yval, zval) = sensor.read_magnetometer()
    #calculating magnetic field strength
    mag = math.sqrt(xval**2 + yval**2 + zval**2)

    #to ensure that the y-value of magnetic field strength remains centered
    spacing = 5-len(str(xval))

    #updating data fields
    xval_label.config(text="x="+str(xval)[0:DIGITS]+" mg"+spacing*" ")
    yval_label.config(text="y="+str(yval)[0:DIGITS]+" mg")
    zval_label.config(text="z="+str(zval)[0:DIGITS]+" mg")
    tot_label.delete("1.0","11.0")
    tot_label.insert("1.0","Total Field Strength = "+str(mag)[0:DIGITS]+" mgauss")

    #updating Window
    root.update()


def main():
    '''provides top-level control. Magnetic field strength readings are constantly updating, and calibration and sensor tests are controlled by the red and black buttons'''

    #setting up device
    setup_ui()
    setup_gpio()
    if (CALONSTART): sensor.calibrate()

    #main loop
    while True:
        #button control
        if (not GPIO.input(23)): sensor.calibrate()
        if (not GPIO.input(24)): sensortest()

        else:                    update_magnetometer()
        time.sleep(0.1)
