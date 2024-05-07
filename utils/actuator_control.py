import RPi.GPIO as GPIO
import time
from .raspberry_setup import *

# def activate_io():
#     # GPIO.output(InputsOutputs.GarageLightOneOnGPIO, GPIO.HIGH)
#     status = GPIO.input(InputsOutputs.GarageLightOneOnGPIO)

#     if status == 1:
#         GPIO.output(InputsOutputs.GarageLightOneOnGPIO, GPIO.LOW)
#         status = GPIO.input(InputsOutputs.GarageLightOneOnGPIO)
#         print(f"GarageLightOneOnGPIO is {status}")
#     else:
#         GPIO.output(InputsOutputs.GarageLightOneOnGPIO, GPIO.HIGH)
#         status = GPIO.input(InputsOutputs.GarageLightOneOnGPIO)
#         print(f"GarageLightOneOnGPIO is {status}")

def toggle_io(deviceId, status):
    # define device with the id map define in raspberry_setup.py file
    # map with raspberry hardware
    device = id_dict[deviceId]
    bool_status = bool(status)

    if bool_status == True:
        print(f"bool_status is {bool_status}")
        GPIO.output(device, GPIO.HIGH)
    else:
        print(f"bool_status is {bool_status}")
        GPIO.output(device, GPIO.LOW)
        status = GPIO.input(deviceId)

    print (GPIO.output(device.deviceId))