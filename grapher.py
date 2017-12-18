#Kaveh Pezeshki
#Dec 16 2017
#Graphing interface with button support

from tkinter import *
import sensor
import time

SIGFIGS=5

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master=master


def setup():
    global root
    global teststat
    global xval_label
    global yval_label
    global zval_label
    #setting up sensor
    sensor.setup_magnetometer()

    #setting up window
    root = Tk()
    root.title("MagnetTest V0.1")
    root.resizable(width=False, height=False)
    root.geometry('{}x{}'.format(320, 240))
    app = Window(root)

    #setting up textboxes

    #user instructions
    instr = Text(root, height=1, width=50)
    instr.tag_configure("center", justify="center")
    instr.insert("1.0","RED=CALIBRATE | BLACK=TEST")
    instr.tag_add("center", "1.0", "end")
    instr.pack()
    #testing status
    teststat = Text(root, height = 1, width=50, font=("Helvetica", 32))
    teststat.tag_configure("center", justify="center")
    teststat.insert("2.0","NO DATA")
    teststat.tag_add("center", "1.0", "end")
    teststat.pack()
    #sensor values
    xval_label = Label(root, text="x=0.000 g", font=("Helvetica",16))
    xval_label.pack(padx=5,pady=10,side=LEFT)
    yval_label = Label(root, text="y=0.000 g", font=("Helvetica",16))
    yval_label.pack(padx=5,pady=10,side=LEFT)
    zval_label = Label(root, text="z=0.000 g", font=("Helvetica",16))
    zval_label.pack(padx=5,pady=10,side=RIGHT)

    root.update()


def update():
    sensor_status = sensor.get_status()
    teststat.delete("1.0","11.0")
    teststat.insert("1.0", sensor_status)

    (xval, yval, zval) = sensor.read_magnetometer()
    xval_label.config(text="x="+str(xval)[0:SIGFIGS]+" g ")
    yval_label.config(text="y="+str(yval)[0:SIGFIGS]+" g")
    zval_label.config(text="z="+str(zval)[0:SIGFIGS]+" g")

    time.sleep(1)
    root.update()



setup()
while True:
    update()
