#!/usr/bin/env python3
import os
import serial
import requests
import json

import tkinter as tk
from tkinter import ttk

import time

# Importing and Naming GPIOs
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

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
# device_is=6128d9c2274a6f001670e7b9
garageLightOneDeviceId = '6128d9c2274a6f001670e7b9'
# device_is=6148cbe49334480016839378
garageLightTwoDeviceId = '6148cbe49334480016839378'
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

    currentLightOneStatus = lightOneStatus
    # runs garageLightOneUpdate every 2 seconds
    root.after(apiRefreshTime, garageLightOneUpdate)


def lightOneSwitch():
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

    currentLightTwoStatus = lightTwoStatus
    # runs garageLightTwoUpdate every 2 seconds
    root.after(apiRefreshTime, garageLightTwoUpdate)


def lightTwoSwitch():
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

# updating GPIOs
def updateGpios():
    # GarageLightOne Handler
    if currentLightOneStatus == True:
        GPIO.output(GarageLightOneOnGPIO, GPIO.HIGH)
    else:
        GPIO.output(GarageLightOneOnGPIO, GPIO.LOW)
    root.after(apiRefreshTime, updateGpios)

    # GarageLightTwo Handler
    if currentLightTwoStatus == True:
        GPIO.output(GarageLightTwoOnGPIO, GPIO.HIGH)
    else:
        GPIO.output(GarageLightTwoOnGPIO, GPIO.LOW)
    root.after(apiRefreshTime, updateGpios)


# function that run all the functions to be ran at the start
def functionUpdates():
    garageLightOneUpdate()
    garageLightTwoUpdate()
    updateGpios()

    # serialExist means arduino is connected and available on USB
    if serialExisit == True:
        temperetureUpdate()


def exit_app():
    root.destroy()


# here starts creating window and main application.
# Create Window
root = tk.Tk()
root.geometry('800x480')


# Temperature Items
temperatureLabel = tk.Label(
    text='Current Room Sensor Temp:',
)
temperatureLabel.pack()

# temperature entry
temperatureEntry = tk.Entry()
temperatureEntry.insert(0, 'loading...')
temperatureEntry.pack()

# light one items
garageLightOneLabel = tk.Label(
    text='Loading...',
    width=15,
    height=2,
)
garageLightOneLabel.pack()

button = tk.Button(
    text='Light One',
    width=15,
    height=1,
    command=lightOneSwitch
)
button.pack()

# light Two items
garageLightTwoLabel = tk.Label(
    text='Loading...',
    width=15,
    height=2,
)
garageLightTwoLabel.pack()

button = tk.Button(
    text='Light Two',
    width=15,
    height=1,
    command=lightTwoSwitch
)
button.pack()

closeButton = tk.Button(
    text='Close',
    width=15,
    height=1,
    command=exit_app
)
closeButton.pack(side='right')

# request functionUpdates to run after 2secs running
root.after(apiRefreshTime, functionUpdates)


# main loop root
root.mainloop()
