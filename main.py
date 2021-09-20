#!/usr/bin/env python3
import os
import serial
import requests
import json

import tkinter as tk
from tkinter import ttk

import time



# project global variables
arduino_temperature_actual = 0
arduino_temperature = 0
currentLightOneStatus = False
serialExisit = False


if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


if serial.Serial('/dev/ttyUSB0', 9600, timeout=1):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()





def temperetureUpdate():

    global arduino_temperature
    if __name__ == '__main__':

        # while True:
        if ser.in_waiting > 0:
            arduino_temperature_actual = float(
                ser.readline().decode('utf-8').rstrip())
            if arduino_temperature + 0.25 < arduino_temperature_actual or arduino_temperature - 0.25 > arduino_temperature_actual:
                arduino_temperature = arduino_temperature_actual

                print(arduino_temperature)
                temperatureEntry.delete(0, 15)
                temperatureEntry.insert(0, arduino_temperature)

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

                print(response.text)
        root.after(500, temperetureUpdate)


def lightOneUpdate():
    global currentLightOneStatus

    url = "https://my-home-automation-api.herokuapp.com/device/6128d9c2274a6f001670e7b9"

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    responseDict = json.loads(response.text)
    lightOneStatus = responseDict['statusBooleanValue']

    if lightOneStatus == True:
        lightOneLabel.config(background='green', text='Light 1 = On')
    else:
        lightOneLabel.config(background='red', text='Light 1 = Off')

    currentLightOneStatus = lightOneStatus
    root.after(2000, lightOneUpdate)

def lightOneSwitch():
    global currentLightOneStatus

    if currentLightOneStatus == True:
        lightOneSwitchTo = False    
    else:
        lightOneSwitchTo = True

    url = "https://my-home-automation-api.herokuapp.com/device/status"

    payload = json.dumps({
        "device": "6128d9c2274a6f001670e7b9",
        "statusValue": "non",
        "statusBooleanValue": lightOneSwitchTo,
        "statusType": "digital"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


# function that run all the functions to be ran at the start
def functionUpdates():
    temperetureUpdate()
    
    lightOneUpdate()
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
temperatureEntry.pack()

# light one items
lightOneLabel = tk.Label(
    text='Loading...',
    width=15,
    height=2,
)
lightOneLabel.pack()

button = tk.Button(
    text='Light One',
    width=25,
    height=5,
    command=lightOneSwitch
)
button.pack()

closeButton = tk.Button(
    text='Close',
    width=25,
    height=5,
    command=exit_app
)
closeButton.pack()

root.after(2000, functionUpdates)


# main loop root
root.mainloop()