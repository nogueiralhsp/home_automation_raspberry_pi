#!/usr/bin/env python3
import serial
import requests
import json

import tkinter as tk
from tkinter import ttk

import time

# ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser = serial.Serial('/dev/tty.usbserial-141120',
                    9600, timeout=1)  # for mac dev
ser.flush()

arduino_temperature_actual = 0
arduino_temperature = 0

light1Status = False


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

    root.after(2000, lightOneUpdate)


# function that run all the functions to be ran at the start
def functionUpdates():
    temperetureUpdate()
    lightOneUpdate()


# Create Window
root = tk.Tk()
root.geometry('300x200')

# Temperature Items
temperatureLabel = tk.Label(
    text='Current Temp:',
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
    text='Click me!',
    width=25,
    height=5,
    command=lightOneUpdate
)
button.pack()

root.after(2000, functionUpdates)


# main loop root
root.mainloop()
