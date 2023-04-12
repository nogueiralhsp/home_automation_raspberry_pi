import os
import serial

arduino_temperature_actual = 0
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
serialExists = False


def arduino_is_present():
    global serialExists
    # checking if there Arduino is connected and USB port is available
    if os.path.exists('/dev/ttyUSB0'):
        global ser
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        ser.flush()
        serialExists = True  # true when arduino is found
        
        return serialExists


def temperatureUpdate():

    
    if os.path.exists('/dev/ttyUSB0'):        
        # receiving data from arduino
        if ser.in_waiting > 0:
            try:
                arduino_temperature_actual = float(
                    ser.readline().decode('utf-8').rstrip())
                ser.flush()
                # print(arduino_temperature_actual) #uncomment for debug
                return arduino_temperature_actual
            except:
                arduino_temperature_actual = 0.00
                # print(arduino_temperature_actual) #uncomment for debug
                return arduino_temperature_actual