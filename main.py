# RELAYS
# 1=> IO 12
# 2=> IO 16
# 3=> IO 20
# 4=> IO 21
# 5=> IO 26
# 6=> IO 19
# 7=> IO 13
# 8=> IO 06
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


# GPIO20
GardenUpperLevelLightGPIO = 16
GPIO.setup(GardenUpperLevelLightGPIO, GPIO.OUT)


# GPIO20
GarageLightTwoOnGPIO = 20
GPIO.setup(GarageLightTwoOnGPIO, GPIO.OUT)

# GPIO21
GarageLightOneOnGPIO = 21
GPIO.setup(GarageLightOneOnGPIO, GPIO.OUT)

# project global variables
arduino_temperature_actual = 0
arduino_temperature = 0
currentLightOneStatus = False
currentLightTwoStatus = False
currentGardenUpperLevelLightStatus = False


# Devices Ids
# garageLightOneDeviceId=6128d9c2274a6f001670e7b9
garageLightOneDeviceId = '6128d9c2274a6f001670e7b9'
# garageLightTwoDeviceId=6148cbe49334480016839378
garageLightTwoDeviceId = '6148cbe49334480016839378'
# gardenUpperLevelLightId="6149904b2f671e0016137975"
gardenUpperLevelLightId = '6149904b2f671e0016137975'

serialExisit = False
apiRefreshTime = 2000  # time to call api for refreshing / call api


# used to run app through SSH
if os.environ.get('DISPLAY', '') == '':
    # print('no display found. Using :0.0') #commented out when don't want to log in terminal
    os.environ.__setitem__('DISPLAY', ':0.0')


# checking if there Arduino is connected and USB port is available
if os.path.exists('/dev/ttyUSB0'):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()
    serialExisit = True  # true when arduino is found


# ***************************************************************************
#                         Garage Handling Functions                         *
# ***************************************************************************
def temperetureUpdate():

    global arduino_temperature
    global serialExisit

    if serialExisit == True:

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
    root.after(500, temperetureUpdate)


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
    # runs garageLightOneUpdate every 2 seconds
    root.after(apiRefreshTime, garageLightOneUpdate)


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

    # runs garageLightTwoUpdate every 2 seconds
    root.after(apiRefreshTime, garageLightTwoUpdate)


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

    # runs garageLightOneUpdate every 2 seconds
    root.after(apiRefreshTime, gardenUpperLevelLightUpdate)


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
    garageLightOneUpdate()
    garageLightTwoUpdate()
    gardenUpperLevelLightUpdate()

    # serialExist means arduino is connected and available on USB
    if serialExisit == True:
        temperetureUpdate()


def exit_app():
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

# request functionUpdates to run after 2secs running
root.after(apiRefreshTime, functionUpdates)


# main loop root
root.mainloop()
