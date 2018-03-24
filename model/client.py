import zmq
import json

def runClient():
    #  Prepare our context and sockets
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    print("connecting to server...")
    socket.connect("tcp://127.0.0.1:5555")
    
    #  Do 10 requests, waiting each time for a response
    for request in range(1,6):
        print("sending message...")
        message = {'content': 'Hello'}
        json_message = json.dumps(message)
        socket.send_string(json_message)
        json_response = socket.recv_string()
        response = json.loads(json_response)
        print("Received reply %s [%s]" % (request, response))
    
    data = ''
    while data != 'exit':
        data = input('Enter something: ')
        message = {'content': data}
        json_message = json.dumps(message)
        socket.send_string(json_message)
        json_response = socket.recv_string()
        response = json.loads(json_response)
        print('Received: %s' % response)
    
    print("sending exit message...")
    message = {'content': 'exit'}
    json_message = json.dumps(message)
    socket.send_string(json_message)
        
if(__name__ == "__main__"):
   runClient()