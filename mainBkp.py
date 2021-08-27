#!/usr/bin/env python3
import serial
import requests
import json




arduino_temperature = 0

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()
    print('im here')
    
    while True:
        if ser.in_waiting > 0:
            arduino_temperature_actual = float(ser.readline().decode('utf-8').rstrip())
            if arduino_temperature + 0.25 < arduino_temperature_actual or arduino_temperature - 0.25 > arduino_temperature_actual:
                arduino_temperature = arduino_temperature_actual
                print(arduino_temperature)

                url = "https://my-home-automation-api.herokuapp.com/device/status"

                payload = json.dumps({
                  "device": "611e35ada7eb2f23a5a86999",
                  "statusValue": arduino_temperature,
                  "statusType": "new temperature"
                })
                headers = {
                  'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)
            
        