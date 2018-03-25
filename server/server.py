import zmq
import time
import json
from model import constants
from model.code_snippet import code_snippet

def runServer():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")
    
    try:
        while True:
            #  Wait for next request from client
            print("waiting for message...")
            json_message = socket.recv_string()
            message = json.loads(json_message)
            print("Received request: %s" % message[constants.MSG_ID])
        
            response = dispatch_message(message)
            json_message = json.dumps(response)
            socket.send_string(json_message)
        
            #time.sleep(0.1)
    except KeyError as e:
        print(e)
        
def dispatch_message(message):
    try:
        if message['id'] == constants.COMMAND_ADD:
            return add_snippet(message)
    except KeyError as badKey:
        return {constants.RESPONSE, 'Bad key: %s' % (badKey.message)}

if(__name__ == "__main__"):
    runServer()
   
def add_snippet(message):
    snippet = code_snippet(message)
    return {constants.RESPONSE: constants.SUCCESS}
    
    
    
