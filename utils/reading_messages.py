import json
from .actuator_control import toggle_io
def read_received_message(message):
    message_dict = json.loads(message)

    print(f"message_dictionary received is {message_dict}")
    
    # if message is a command
    if message_dict['messageType'] == 'command':

        # if device is digital

        if message_dict['statusType'] =='digital':
            # print('statusType is digital')
            # toggle io will toggle on/off the io
            toggle_io('device_'+message_dict['device'], message_dict['statusBooleanValue'])
            
        # if device is analog
        # elif message_dict['statusType'] =='analog':
            # print('statusType is analog')
        # else:
            # print('statusType is not digital nor analog')