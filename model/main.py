from threading import Thread
import time
from model.server import runServer
from model.client import runClient

def main():
    server = Thread(target=runServer)
    client = Thread(target=runClient)
    print("main - starting server")
    server.start()
    print("main - waiting for server to start")
    time.sleep(1)
    print("main - starting client")
    client.start()
    
    while(server.is_alive() or client.is_alive()):
        time.sleep(1)
        
    return
    
    
if(__name__ == "__main__"):
    main()