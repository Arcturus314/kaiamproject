#Kaveh Pezeshki
#Dec 16 2017
#Graphing interface for isolator project with button support


#imports
from tkinter import *
import sensor
import time
import RPi.GPIO as GPIO
import math
from PIL import ImageTk
from PIL import Image

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
    #setting up sensor
    sensor.setup_magnetometer()


def setup_ui():
    '''Adds UI elements to Window'''

    #declaring fields as global
    global root
    global teststat
    global xval_label
    global yval_label
    global zval_label
    global tot_label
    global xoff_label
    global yoff_label
    global zoff_label

    #to prevent image from being garbage collected
    global logo
    global logo_panel

    #setting up window parameters
    root = Tk()
    root.title("MagnetTest V0.1")
    root.attributes('-fullscreen', True)
    app = Window(root)

    #setting up textboxes

    #inserting Kaiam logo
    logo = ImageTk.PhotoImage(Image.open("/home/pi/kaiamproject/kaiam.png"))
    logo_panel = Label(root, image=logo)
    logo_panel.logo = logo
    logo_panel.grid(row=0,column=0)
    #user instructions
    instr = Label(root, text="RED=CALIBRATE | BLACK=TEST", font=("Helvetica", 20))
    instr.grid(row=0, column=1, columnspan=2)
    #testing status
    teststat = Label(root, text="NO DATA", font=("Helvetica", 42))
    teststat.configure(foreground="orange")
    teststat.grid(row=1, column=0, columnspan=3)
    #sensor magnitude
    spacer_1  = Label(root, text=" ").grid(row=2,column=1)
    tot_label = Label(root, text="Total Field Strength = 0.000 mgauss", font=("Helvetica", 30))
    tot_label.grid(row=3, column=0, columnspan=3)
    #sensor values
    sensor_label = Label(root, font=("Helvetica", 26), text=u"Current \u0394 From Offset")
    sensor_label.grid(row=4, column=0, columnspan=3)
    xval_label = Label(root, text="x=0.000 mg", font=("Helvetica",26))
    xval_label.grid(row=5,column=0)
    yval_label = Label(root, text="y=0.000 mg", font=("Helvetica",26))
    yval_label.grid(row=5,column=1)
    zval_label = Label(root, text="z=0.000 mg", font=("Helvetica",26))
    zval_label.grid(row=5,column=2)
    #offset values
    offset_label = Label(root, font=("Helvetica", 26), text="Offset Values")
    offset_label.grid(row=6, column=0, columnspan=3)
    xoff_label = Label(root, text="x=0.000 mg", font=("Helvetica",26))
    xoff_label.grid(row=7,column=0)
    yoff_label = Label(root, text="y=0.000 mg", font=("Helvetica",26))
    yoff_label.grid(row=7,column=1)
    zoff_label = Label(root, text="z=0.000 mg", font=("Helvetica",26))
    zoff_label.grid(row=7,column=2)
    #updating Window
    root.update()

def sensortest():
    '''reads sensor data and updates Window fields, as well as calculating whether the tested isolator is in spec'''

    #reading the magnetometer
    (xval, yval, zval) = sensor.read_magnetometer()
    sensor.calc_status((xval, yval, zval))
    sensor_status = sensor.get_status()

    #setting the sensor status field
    teststat.configure(text=sensor_status)

    #updating the sensor status field color
    if sensor_status == "INIT FAILED" or sensor_status == "TEST FAILED":
        teststat.configure(foreground="red")
    elif sensor_status == "NO DATA":
        teststat.configure(foreground="orange")
    elif sensor_status == "TEST PASSED":
        teststat.configure(foreground="green")

    #updating magnetic field strength measurements and Window
    update_magnetometer()

def update_offsets():
    '''reads offsets and updates Window fields'''
    #reading offset data
    (xoff, yoff, zoff) = sensor.get_offsets()

    #updating data fields
    xoff_label.config(text="x="+str(xoff)[0:DIGITS]+" mg")
    yoff_label.config(text="y="+str(yoff)[0:DIGITS]+" mg")
    zoff_label.config(text="z="+str(zoff)[0:DIGITS]+" mg")

    #updating Window
    root.update()

def update_magnetometer():
    '''reads sensor data and updates Window fields'''

    #reading magnetometer data
    (xval, yval, zval) = sensor.read_magnetometer()
    #calculating magnetic field strength
    mag = math.sqrt(xval**2 + yval**2 + zval**2)

    #updating data fields
    xval_label.config(text="x="+str(xval)[0:DIGITS]+" mg")
    yval_label.config(text="y="+str(yval)[0:DIGITS]+" mg")
    zval_label.config(text="z="+str(zval)[0:DIGITS]+" mg")
    tot_label.configure(text="Total Field Strength = "+str(mag)[0:DIGITS]+" mgauss")

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
        if (not GPIO.input(23)):
            sensor.calibrate()
            update_offsets()
        if (GPIO.input(24)):
            sensortest()
        else:
            update_magnetometer()
        time.sleep(0.1)

main()
