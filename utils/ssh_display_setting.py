import os

def ssh_display():
    # used to run app through SSH
    if os.environ.get('DISPLAY', '') == '':
        # print('no display found. Using :0.0') #commented out when don't want to log in terminal
        os.environ.__setitem__('DISPLAY', ':0.0')
