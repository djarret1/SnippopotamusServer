import zmq
import time
import json
from model import constants
from model.code_snippet import Code_Snippet

user_file = '../server/users.txt'
users = set()

def load_users():
    with open(user_file) as inputFile:
        for user in inputFile:
            users.add(user.strip())

def runServer():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")
    load_users()
    
    print(users)
    while True:
        #  Wait for next request from client
        print("waiting for message...")
        json_message = socket.recv_string()
        message = json.loads(json_message)
        
        try:
            print("Received request: %s" % message[constants.MSG_ID])
            print("From: %s" % message[constants.MSG_USER_NAME])
            
            if not validate_user(message, users) and message[constants.MSG_ID] != constants.COMMAND_NEW_USER:
                send_response(constants.INVALID_USER, socket)
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
    if message[constants.MSG_ID] == constants.COMMAND_NEW_USER:
        return add_user(message)
    return send_response(constants.UNKNOWN_ID + ': ' + message[constants.MSG_ID])

def add_snippet(message):
    snippet = Code_Snippet(message)
    return {constants.RESPONSE: constants.SUCCESS}

def add_user(message):
    if message[constants.MSG_USER_NAME] in users:
        return {constants.RESPONSE: constants.USER_EXISTS}
    users.add(message[constants.MSG_USER_NAME])
    with open(user_file, 'a') as output_file:
        output_file.write(message[constants.MSG_USER_NAME] + '\n')
    return {constants.RESPONSE: constants.SUCCESS}

def send_response(fail_type, socket):
    response = json.dumps( {constants.RESPONSE: fail_type} )
    socket.send_string(response)

def validate_user(message, users):
    if message[constants.MSG_USER_NAME] in users:
        return True
    return False

if(__name__ == "__main__"):
    runServer()
