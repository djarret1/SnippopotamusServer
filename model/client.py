import time
import zmq
import json
from model import constants

user_Id = 'admin'

def runClient():
    #  Prepare our context and sockets
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    print("connecting to server...")
    socket.connect("tcp://127.0.0.1:5555")
    
#     name = input('Name: ')
#     desc = input('Description: ')
#     code = input('Code: ')
#     tags = []
#     count = int(input('How many tags: '))
#     for i in range(0, count):
#         tag = input('Enter tag: ')
#         tags.append(tag)
#            
#     message = {constants.MSG_ID: constants.COMMAND_ADD,
#                constants.MSG_USER_NAME: user_Id,
#                constants.MSG_NAME: name,
#                constants.MSG_DESC: desc,
#                constants.MSG_CODE: code,
#                constants.MSG_TAGS: tags}
 
#     message = {constants.MSG_ID: constants.COMMAND_NEW_USER,
#                constants.MSG_USER_NAME: 'newguy'}
    
    message = {constants.MSG_ID: constants.COMMAND_DUMP,
               constants.MSG_USER_NAME: user_Id}
    
    time.sleep(0.5)
    
    json_message = json.dumps(message)
    socket.send_string(json_message)
    json_response = socket.recv_string()
    response = json.loads(json_response)
    
    print(response)
    
    time.sleep(0.5)
    message = {constants.MSG_ID: constants.COMMAND_TERMINATE, constants.MSG_USER_NAME: user_Id}
    
    json_message = json.dumps(message)
    socket.send_string(json_message)
    json_response = socket.recv_string()
    response = json.loads(json_response)
       
    print(response)
        
if(__name__ == "__main__"):
   runClient()