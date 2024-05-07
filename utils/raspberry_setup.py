import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
# RELAYS
# 1=> IO 12 = WorkbenchLightGPIO
# 2=> IO 16 = GarageLightOneOnGPIO
# 3=> IO 20 = GarageLightTwoOnGPIO
# 4=> IO 21 = GardenUpperLevelLightGPIO
# 5=> IO 26 =
# 6=> IO 19 =
# 7=> IO 13 =
# 8=> IO 06 =


# dictionary with id for the devices
id_dict = {
    'device_61542f1bd06971001641672f': 12,
    'device_6149904b2f671e0016137975': 21
}

# starting up raspberry pi ios config
def starting_up():
    print('*** starting up raspberry_setup_pi ***')
    GPIO.setwarnings(False)
    # GPIO12
    WorkbenchLightGPIO = 12
    GPIO.setup(WorkbenchLightGPIO, GPIO.OUT)

    # GPIO16 - Upper Level Garden Light
    GPIO.setup(id_dict['device_6149904b2f671e0016137975'], GPIO.OUT)
