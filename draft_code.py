import os
import serial

# for mac dev
# if serial.Serial('/dev/tty.usbserial-142130'):
#     serialExisit = True
#     ser = serial.Serial('/dev/tty.usbserial-142130',9600, timeout=1)  
#     ser.flush()

print (os.path.exists('/dev/tty.usbserial-142130'))