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
import os
from tkinter.constants import S
import serial
import requests
import json


import tkinter as tk
from tkinter import *

import time

# Importing and Naming GPIOs
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


# GPIO12
WorkbenchLightGPIO = 12
GPIO.setup(WorkbenchLightGPIO, GPIO.OUT)


# GPIO20
GarageLightOneOnGPIO = 16
GPIO.setup(GarageLightOneOnGPIO, GPIO.OUT)

# GPIO21
GarageLightTwoOnGPIO = 20
GPIO.setup(GarageLightTwoOnGPIO, GPIO.OUT)


# GPIO16
GardenUpperLevelLightGPIO = 21
GPIO.setup(GardenUpperLevelLightGPIO, GPIO.OUT)

# project global variables
arduino_temperature_actual = 0
arduino_temperature = 0

currentLightWorkbenchStatus = False
currentLightOneStatus = False
currentLightTwoStatus = False
currentGardenUpperLevelLightStatus = False


# Devices Ids
# garageLightWorkbenchDeviceId ='61542f1bd06971001641672f'
garageLightWorkbenchDeviceId = '61542f1bd06971001641672f'
# garageLightOneDeviceId=6128d9c2274a6f001670e7b9
garageLightOneDeviceId = '6128d9c2274a6f001670e7b9'
# garageLightTwoDeviceId=6148cbe49334480016839378
garageLightTwoDeviceId = '6148cbe49334480016839378'
# gardenUpperLevelLightId="6149904b2f671e0016137975"
gardenUpperLevelLightId = '6149904b2f671e0016137975'

serialExists = False
apiRefreshTime = 2000  # time to call api for refreshing / call api


# used to run app through SSH
if os.environ.get('DISPLAY', '') == '':
    # print('no display found. Using :0.0') #commented out when don't want to log in terminal
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
    url = "https://my-home-automation-api.herokuapp.com"

    try:
        request = requests.get(url, timeout = timeoutCheck)
        # print("connected to the internet")
        internetConnectionExists = True

        if internetConnectionExists == True:
            onlineStatus.config(background='green', text='We are on-line')
        else:
            onlineStatus.config(background='red', text='We are off-line')

    except (requests.ConnectionError, requests.Timeout) as exception:
        # print("no internet connection")
        internetConnectionExists = False

    return internetConnectionExists

# ***************************************************************************
#                         Garage Handling Functions                         *
# ***************************************************************************


def temperetureUpdate():

    global arduino_temperature

    if serialExists == True:

        # while True:
        if ser.in_waiting > 0:
            arduino_temperature_actual = float(
                ser.readline().decode('utf-8').rstrip())
            if arduino_temperature + 0.25 < arduino_temperature_actual or arduino_temperature - 0.25 > arduino_temperature_actual:
                arduino_temperature = arduino_temperature_actual

                print(arduino_temperature)  # loging on terminal for debug
                temperatureEntry.delete(0, 'end')
                temperatureEntry.insert(
                    0, '         '+str(arduino_temperature)+(' °C'))  # inserting to entry component

            
                url = "https://my-home-automation-api.herokuapp.com/device/status"

                payload = json.dumps({
                    "device": "611e35ada7eb2f23a5a86999",
                    "statusValue": arduino_temperature,
                    "statusBooleanValue": False,
                    "statusType": "analog"
                })
                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.request(
                    "POST", url, headers=headers, data=payload)

                print(response.text)  # logging response from api
    else:
        print("Equipment offline. Loging on screen only " , arduino_temperature," °C")  # loging on terminal for debug

    root.after(500, temperetureUpdate)


# # ***************************************************************************
def garageLightWorkbenchUpdate():
    global currentLightWorkbenchStatus
    global garageLightWorkbenchDeviceId

    url = "https://my-home-automation-api.herokuapp.com/device/" + \
        garageLightWorkbenchDeviceId

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    responseDict = json.loads(response.text)
    lightWorkbenchStatus = responseDict['statusBooleanValue']

    if lightWorkbenchStatus == True:
        garageLightWorkbenchLabel.config(
            background='green', text='Workbench = On')
    else:
        garageLightWorkbenchLabel.config(
            background='red', text='Workbench = Off')

    if currentLightWorkbenchStatus != lightWorkbenchStatus:
        currentLightWorkbenchStatus = lightWorkbenchStatus
        updateGarageLightWorkbenchGpio(
            currentLightWorkbenchStatus)  # updating GPIO


def lightWorkbenchSwitch():  # used when pressed button on screen
    global currentLightWorkbenchStatus
    global garageLightWorkbenchDeviceId

    if currentLightWorkbenchStatus == True:
        lightWorkbenchSwitchTo = False
    else:
        lightWorkbenchSwitchTo = True

    url = "https://my-home-automation-api.herokuapp.com/device/status"

    payload = json.dumps({
        "device": garageLightWorkbenchDeviceId,
        "statusValue": "non",
        "statusBooleanValue": lightWorkbenchSwitchTo,
        "statusType": "digital"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def updateGarageLightWorkbenchGpio(lightStatus):
    # GarageLightOne Handler
    if lightStatus == True:
        GPIO.output(WorkbenchLightGPIO, GPIO.HIGH)
    else:
        GPIO.output(WorkbenchLightGPIO, GPIO.LOW)
# # ***************************************************************************


def garageLightOneUpdate():
    global currentLightOneStatus
    global garageLightOneDeviceId

    url = "https://my-home-automation-api.herokuapp.com/device/"+garageLightOneDeviceId

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    responseDict = json.loads(response.text)
    lightOneStatus = responseDict['statusBooleanValue']

    if lightOneStatus == True:
        garageLightOneLabel.config(background='green', text='Light 1 = On')
    else:
        garageLightOneLabel.config(background='red', text='Light 1 = Off')

    if currentLightOneStatus != lightOneStatus:
        currentLightOneStatus = lightOneStatus
        updateGarageLightOneGpio(currentLightOneStatus)  # updating GPIO


def lightOneSwitch():  # used when pressed button on screen
    global currentLightOneStatus

    if currentLightOneStatus == True:
        lightOneSwitchTo = False
    else:
        lightOneSwitchTo = True

    url = "https://my-home-automation-api.herokuapp.com/device/status"

    payload = json.dumps({
        "device": garageLightOneDeviceId,
        "statusValue": "non",
        "statusBooleanValue": lightOneSwitchTo,
        "statusType": "digital"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def updateGarageLightOneGpio(lightStatus):
    # GarageLightOne Handler
    if lightStatus == True:
        GPIO.output(GarageLightOneOnGPIO, GPIO.HIGH)
    else:
        GPIO.output(GarageLightOneOnGPIO, GPIO.LOW)


def garageLightTwoUpdate():
    global garageLightTwoDeviceId
    global currentLightTwoStatus

    url = "https://my-home-automation-api.herokuapp.com/device/"+garageLightTwoDeviceId

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    responseDict = json.loads(response.text)
    lightTwoStatus = responseDict['statusBooleanValue']

    if lightTwoStatus == True:
        garageLightTwoLabel.config(background='green', text='Light 2 = On')
    else:
        garageLightTwoLabel.config(background='red', text='Light 2 = Off')

    if currentLightTwoStatus != lightTwoStatus:
        currentLightTwoStatus = lightTwoStatus
        updateGarageLightTwoGpio(currentLightTwoStatus)  # updating GPIO


def lightTwoSwitch():  # used when pressed button on screen
    global currentLightTwoStatus

    if currentLightTwoStatus == True:
        lightTwoSwitchTo = False
    else:
        lightTwoSwitchTo = True

    url = "https://my-home-automation-api.herokuapp.com/device/status"

    payload = json.dumps({
        "device": garageLightTwoDeviceId,
        "statusValue": "non",
        "statusBooleanValue": lightTwoSwitchTo,
        "statusType": "digital"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def updateGarageLightTwoGpio(lightStatus):
    # GarageLightTwo Handler
    if lightStatus == True:
        GPIO.output(GarageLightTwoOnGPIO, GPIO.HIGH)
    else:
        GPIO.output(GarageLightTwoOnGPIO, GPIO.LOW)


# ***************************************************************************
#                         Garden Handling Functions                         *
# ***************************************************************************

def gardenUpperLevelLightUpdate():
    global currentGardenUpperLevelLightStatus
    global gardenUpperLevelLightId

    url = "https://my-home-automation-api.herokuapp.com/device/"+gardenUpperLevelLightId

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    responseDict = json.loads(response.text)
    # light status from server (data base)
    gardenUpperLevelLightStatus = responseDict['statusBooleanValue']

    if gardenUpperLevelLightStatus == True:
        upperLevelLightLabel.config(background='green', text='Light 1 = On')
    else:
        upperLevelLightLabel.config(background='red', text='Light 1 = Off')

    if gardenUpperLevelLightStatus != currentGardenUpperLevelLightStatus:
        currentGardenUpperLevelLightStatus = gardenUpperLevelLightStatus
        updateGardenUpperLevelLightGpio(
            currentGardenUpperLevelLightStatus
        )  # updating GPIO


def gardenUpperLevelLightSwitch():  # used when pressed button on screen
    global currentGardenUpperLevelLightStatus

    if currentGardenUpperLevelLightStatus == True:
        gardenUpperLevelLightSwitchTo = False
    else:
        gardenUpperLevelLightSwitchTo = True

    url = "https://my-home-automation-api.herokuapp.com/device/status"

    payload = json.dumps({
        "device": gardenUpperLevelLightId,
        "statusValue": "non",
        "statusBooleanValue": gardenUpperLevelLightSwitchTo,
        "statusType": "digital"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def updateGardenUpperLevelLightGpio(lightStatus):
    # GarageLightTwo Handler
    if lightStatus == True:
        GPIO.output(GardenUpperLevelLightGPIO, GPIO.HIGH)
    else:
        GPIO.output(GardenUpperLevelLightGPIO, GPIO.LOW)


# function that run all the functions to be ran at the start
def functionUpdates():
    global internetConnectionExists
    # serialExist means arduino is connected and available on USB
    if serialExists == True:
        temperetureUpdate()

    if internetConnectionCheck():
        garageLightOneUpdate()
        garageLightTwoUpdate()
        gardenUpperLevelLightUpdate()
        garageLightWorkbenchUpdate()


# Updating all GPIOs at the start
# they are all kept off for manual use of lights
    updateGarageLightOneGpio(currentLightOneStatus)
    updateGarageLightTwoGpio(currentLightTwoStatus)
    updateGarageLightWorkbenchGpio(currentLightWorkbenchStatus)
    updateGardenUpperLevelLightGpio(currentGardenUpperLevelLightStatus)

    # request functionUpdates to run after 2secs running
    root.after(apiRefreshTime, functionUpdates)


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
garageFrame = LabelFrame(
    mainContainerFrame,
    text='Garage Controls',
    width=100,
    height=100,
    # bg="#331a00"
)
garageFrame.pack(
    fill="both",
    expand="yes",
    side="left"
)

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

bottomControls = Frame(
    root,
    height=1
)
bottomControls.pack(
    side='top',
    fill='both',
    expand='yes',

)

#
# Status Components
onlineStatus = Label(
    statusFrame,
    text='Loading...',
    width=lableWidth,
    height=lableHeigh,
)
onlineStatus.pack()

# Temperature Items
temperatureLabel = Label(
    garageFrame,
    text="Current Room Sensor Temp:",
)
temperatureLabel.pack()

# temperature entry
temperatureEntry = Entry(
    garageFrame,
    width=15
)
temperatureEntry.insert(0, 'loading...')
temperatureEntry.pack()

# light one items
garageLightOneLabel = Label(
    garageFrame,
    text='Loading...',
    width=lableWidth,
    height=lableHeigh,
)
garageLightOneLabel.pack()

lightOneButton = Button(
    garageFrame,
    text='Light One',
    width=buttonWidth,
    height=buttonHeight,
    command=lightOneSwitch
)
lightOneButton.pack()

# light Two items
garageLightTwoLabel = Label(
    garageFrame,
    text='Loading...',
    width=lableWidth,
    height=lableHeigh,
)
garageLightTwoLabel.pack()

lightTwoButton = Button(
    garageFrame,
    text='Light Two',
    width=buttonWidth,
    height=buttonHeight,
    command=lightTwoSwitch
)
lightTwoButton.pack()


# light Workbench items
garageLightWorkbenchLabel = Label(
    garageFrame,
    text='Loading...',
    width=lableWidth,
    height=lableHeigh,
)
garageLightWorkbenchLabel.pack()

lightWorkbenchButton = Button(
    garageFrame,
    text='Workbench',
    width=buttonWidth,
    height=buttonHeight,
    command=lightWorkbenchSwitch
)
lightWorkbenchButton.pack()

# Garden components
upperLevelLightLabel = Label(
    gardenFrame,
    text='Loading...',
    width=lableWidth,
    height=lableHeigh,
)
upperLevelLightLabel.pack()

upperLevelLightButton = Button(
    gardenFrame,
    text='Upper Level',
    width=buttonWidth,
    height=buttonHeight,
    command=gardenUpperLevelLightSwitch
)
upperLevelLightButton.pack()


# close window/application button
closeButton = Button(
    root,
    text='Close',
    width=buttonWidth,
    height=buttonHeight,
    command=exit_app
)
closeButton.pack(side='bottom')

root.after(apiRefreshTime, functionUpdates)

# main loop root
root.mainloop()
