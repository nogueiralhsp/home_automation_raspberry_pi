#!/usr/bin/env python3
# RELAYS
# 1=> IO 12 = WorkbenchLightGPIO
# 2=> IO 16 = GardenUpperLevelLightGPIO
# 3=> IO 20 = GarageLightOneOnGPIO
# 4=> IO 21 = GarageLightTwoOnGPIO
# 5=> IO 26 =
# 6=> IO 19 =
# 7=> IO 13 =
# 8=> IO 06 =
#
#!/usr/bin/env python3

from utils.ssh_display_setting import *
from tkinter.constants import S
import serial
import requests
import json

from utils.raspberry_setup import *

import tkinter as tk
from tkinter import *

# Importing and Naming GPIOs
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# value for server url
apiurl = 'http://192.168.0.28:9000'

# declaring gios
# GPIO12
WorkbenchLightGPIO = 12
GPIO.setup(WorkbenchLightGPIO, GPIO.OUT)

# GPIO21
GardenUpperLevelLightGPIO = 21
GPIO.setup(GardenUpperLevelLightGPIO, GPIO.OUT)

# project global variables
# arduino reading variables
arduino_temperature_actual = 0
arduino_temperature = 0

# light status variables
currentLightWorkbenchStatus = False
currentLightOneStatus = False
currentLightTwoStatus = False
currentGardenUpperLevelLightStatus = False

# Devices Ids
# garageTemperatureDeviceId = '611e4cdb50cf940016c86c0b'
garageTemperatureDeviceId = '611e4cdb50cf940016c86c0b'
# garageLightWorkbenchDeviceId ='61542f1bd06971001641672f'
garageLightWorkbenchDeviceId = '61542f1bd06971001641672f'
# garageLightOneDeviceId=6128d9c2274a6f001670e7b9
garageLightOneDeviceId = '6128d9c2274a6f001670e7b9'
# garageLightTwoDeviceId=6148cbe49334480016839378
garageLightTwoDeviceId = '6148cbe49334480016839378'
# gardenUpperLevelLightId="6149904b2f671e0016137975"
gardenUpperLevelLightId = '6149904b2f671e0016137975'

# serial connection
serialExists = False
apiRefreshTime = 10000  # time to call api for refreshing / call api

# used to run app through SSH
if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0') #commented out when don't want to log in terminal
    os.environ.__setitem__('DISPLAY', ':0.0')

# checking if there Arduino is connected and USB port is available
if os.path.exists('/dev/ttyUSB0'):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()
    serialExists = True  # true when arduino is found

# Checking internet connection
# returns true if there internet connection is on
def internetConnectionCheck():
    timeoutCheck = 0.5
    # url = apiurl+""
    url=apiurl

    try:
        request = requests.get(url, timeout=timeoutCheck)
        internetConnectionExists = True

        if internetConnectionExists == True:
            onlineStatus.config(background='green', text='We are on-line')
        else:
            onlineStatus.config(background='red', text='We are off-line')

    except (requests.ConnectionError, requests.Timeout) as exception:
        print("no internet connection")
        internetConnectionExists = False

    return internetConnectionExists

# ***************************************************************************
#                         Garage Handling Functions                         *
# ***************************************************************************
def temperetureUpdate():
    # delta is the difference between the actual temperature and the last temperature
    # this value is used to trigger the logging function
    deltaTemperature = 0.5
    global arduino_temperature
    global garageTemperatureDeviceId

    if serialExists == True:

        # while True:
        if ser.in_waiting > 0:
            try:
                arduino_temperature_actual = float(
                    ser.readline().decode('utf-8').rstrip())
            except:
                arduino_temperature_actual = 0.00

            if arduino_temperature + deltaTemperature < arduino_temperature_actual or arduino_temperature - deltaTemperature > arduino_temperature_actual:
                arduino_temperature = arduino_temperature_actual

                print(f'Garage room temperature {arduino_temperature}')  # loging on terminal for debug
                # temperature entry is the var for temperature field on interface
                temperatureEntry.delete(0, 'end')
                temperatureEntry.insert(
                    0, '         '+str(arduino_temperature)+(' °C'))  # inserting to entry component

                url = apiurl+"/device/status"

                payload = json.dumps({
                    "device": garageTemperatureDeviceId,
                    "statusValue": arduino_temperature,
                    "statusBooleanValue": False,
                    "statusType": "analog"
                })
                headers = {
                    'Content-Type': 'application/json'
                }
                try:
                    response = requests.request(
                        "POST", url, headers=headers, data=payload)

                    
                except requests.exceptions.RequestException as e:  # This is the correct syntax
                    print(f'this is the error from api {e}')  # logging response from api
                    raise SystemExit(e)
    else:
        print("Equipment offline. Loging on screen only ",
            arduino_temperature, " °C")  # loging on terminal for debug

    root.after(500, temperetureUpdate)
# updating GPIO
def updateGarageLightWorkbenchGpio(lightStatus):
    # GarageLightOne Handler
    if lightStatus == True:
        GPIO.output(WorkbenchLightGPIO, GPIO.HIGH)
    else:
        GPIO.output(WorkbenchLightGPIO, GPIO.LOW)

# new button test function
def upperLightsHandler():
    # Read the status of the Garden Upper Level
    status =  GPIO.input(GardenUpperLevelLightGPIO)
    # GarageLightTwo Handler
    if status == True:
        print("upper lights handler on, turning off")
        GPIO.output(GardenUpperLevelLightGPIO, GPIO.LOW)
        upperLightLabel.config(text='Lights Off')
        upperLightLabel.config(background='red')
        upperLightLabel.config(foreground='white')
    else:
        print("upper lights handler off, turning on")
        GPIO.output(GardenUpperLevelLightGPIO, GPIO.HIGH)
        upperLightLabel.config(text='Lights On')
        upperLightLabel.config(background='green')
        upperLightLabel.config(foreground='white')

    # next to do, send status to API via websocket

def exit_app():
    GPIO.cleanup()
    root.destroy()


# ***************************************************************************
#              here starts creating window and main application.            *
# ***************************************************************************
# vars used on GUI
lableWidth = 15
lableHeigh = 1
buttonWidth = 15
buttonHeight = 1


# Create Window
ssh_display()
root = tk.Tk()
root.geometry('400x480')
mainContainerFrame = Frame(
    root
)
mainContainerFrame.pack(
    fill='both',
    side='top',
    expand='yes'
)
statusFrame = LabelFrame(
    mainContainerFrame,
    text='Status',
    width=100,
    height=10,
    # bg="#331a00"
)
statusFrame.pack(
    fill="both",
    expand="yes",
)
# garden frame
gardenFrame = LabelFrame(
    mainContainerFrame,
    text='Garden Controls',
    width=100,
    height=100,
    # bg="red"
)
gardenFrame.pack(
    fill='both',
    side='left',
    expand='yes'
)

############################################
# Status Components
onlineStatus = Label(
    statusFrame,
    text='Loading...',
    width=lableWidth,
    height=lableHeigh,
)
onlineStatus.pack()
# temperature entry
temperatureEntry = Entry(
    statusFrame,
    width=15
)
temperatureEntry.insert(0, 'loading...')
temperatureEntry.pack()
# light Workbench items
upperLightLabel = Label(
    gardenFrame,
    text='Lights Off',
    width=lableWidth,
    height=lableHeigh,
    background='red',
    foreground='white'
)
upperLightLabel.pack()
upperLightButton = Button(
    gardenFrame,
    text='Upper Garden',
    width=buttonWidth,
    height=buttonHeight,
    command=upperLightsHandler
)
upperLightButton.pack()
############################################
# close window/application button
closeButton = Button(
    root,
    text='Close',
    width=buttonWidth,
    height=buttonHeight,
    command=exit_app
)
closeButton.pack(side='bottom')
def functionUpdates():
    global internetConnectionExists

    # serialExist means arduino is connected and available on USB
    if serialExists == True:
        temperetureUpdate()
    # check if there is connection to the api server
    internetConnectionCheck()
    # request functionUpdates to run after 2secs running
    root.after(apiRefreshTime, functionUpdates)
    
root.after(apiRefreshTime, functionUpdates)
# main loop
if __name__ == "__main__":
    # main loop root
    while True:
        root.mainloop()