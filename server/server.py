import zmq
import time
import json
from model import constants
from model.code_snippet import Code_Snippet

def runServer():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")
    
    while True:
        #  Wait for next request from client
        print("waiting for message...")
        json_message = socket.recv_string()
        message = json.loads(json_message)
        
        try:
            print("Received request: %s" % message[constants.MSG_ID])
            print("From: %s" % message[constants.MSG_USER_NAME])
            
            if not validate_user(message):
                response = send_response(constants.INVALID_USER, socket)
            else:
                process_message(message, socket)
        except KeyError as e:
            send_response(constants.MISSING_KEY + ': ' + str(e), socket)
        
def process_message(message, socket):
    try:
        response = dispatch_message(message)
        json_message = json.dumps(response)
        socket.send_string(json_message)
    except KeyError as e:
        send_response(str(e), socket)

def dispatch_message(message):
    if message[constants.MSG_ID] == constants.COMMAND_ADD:
        return add_snippet(message)
    return send_response(constants.UNKNOWN_ID + ': ' + message[constants.MSG_ID])

def add_snippet(message):
    snippet = Code_Snippet(message)
    return {constants.RESPONSE: constants.SUCCESS}
    
def send_response(fail_type, socket):
    response = json.dumps( {constants.RESPONSE: fail_type} )
    socket.send_string(response)

def validate_user(message):
    #Todo
    if message[constants.MSG_USER_NAME] == 'jdk600':
        return True
    return False

if(__name__ == "__main__"):
    runServer()
