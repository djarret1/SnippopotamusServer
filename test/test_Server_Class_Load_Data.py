'''
Created on Mar 27, 2018

@author: jdk60
'''
from threading import Thread
import unittest
import model.constants as constants
from server.server import Server
import os
import zmq
import time
import json


user_file = 'users.txt'
snippet_file = 'snippets.txt'
ip_port = "tcp://127.0.0.1:5555"

class Test(unittest.TestCase):

    def setUp(self):
        with open('snippets.txt', 'w') as output_file:
            output_file.write('admin,test,test,test,test,needs_approval\n' +
                              'admin,test1,test1,test1,test1,needs_approval\n' + 
                              'admin,Bubble,Sort,code,test1,tag2,needs_approval\n')
        
        Thread(target=self.runServer).start()
        time.sleep(1)
         
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REQ)
        self._socket.connect(ip_port)
    
    def tearDown(self):
        message = {constants.MSG_ID: constants.COMMAND_TERMINATE,
                   constants.MSG_USER_NAME: constants.USR_ADMIN}
        json_message = json.dumps(message) 
        self._socket.send_string(json_message)
        
    def runServer(self, ip=ip_port):
        Server(ip, users_file=user_file, snippets_file=snippet_file).main_loop()
    
    def testLoadServerWithExistingSnippetData(self):
        message = {constants.MSG_ID: constants.COMMAND_DUMP,
                   constants.MSG_USER_NAME: constants.USR_ADMIN}
        json_message = json.dumps(message)
        self._socket.send_string(json_message)
        
        json_response = self._socket.recv_string()
        response = json.loads(json_response)
        
        self.assertTrue('test' in response[constants.RESPONSE])
        self.assertTrue('test1' in response[constants.RESPONSE])
        self.assertTrue('Bubble' in response[constants.RESPONSE])