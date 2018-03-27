'''
Created on Mar 26, 2018

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

user_file = './test/users.txt'
snippet_file = './test/snippets.txt'
ip_port = "tcp://127.0.0.1:5555"

class Test(unittest.TestCase):

    def setUp(self):
        if os.path.isfile(user_file):
            os.remove(user_file)
        if os.path.isfile(snippet_file):
            os.remove(snippet_file)
        
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

    def runServer(self):
        Server(ip_port, users_file=user_file, snippets_file=snippet_file).main_loop()
    
    def testAddingASnippet(self):
        snippet_name = 'test_snippet'
        snippet_desc = 'test_desc'
        snippet_code = 'test_code'
        snippet_tags = ['test1', 'test2']
        
        message = {constants.MSG_ID: constants.COMMAND_ADD,
                   constants.MSG_USER_NAME: constants.USR_ADMIN,
                   constants.MSG_NAME: snippet_name,
                   constants.MSG_DESC: snippet_desc,
                   constants.MSG_CODE: snippet_code,
                   constants.MSG_TAGS: snippet_tags}
        
        json_message = json.dumps(message)
        self._socket.send_string(json_message)
        json_response = self._socket.recv_string()
        response = json.loads(json_response)
        self.assertTrue(response[constants.RESPONSE] == constants.SUCCESS)
        
        message = {constants.MSG_ID: constants.COMMAND_DUMP,
                   constants.MSG_USER_NAME: constants.USR_ADMIN}
        json_message = json.dumps(message)
        self._socket.send_string(json_message)
        json_response = self._socket.recv_string()
        response = json.loads(json_response)
        
        embedded_record = response[constants.RESPONSE]
        self.assertTrue(snippet_name in embedded_record, 'checking to make sure the name is present')
        self.assertTrue(snippet_desc in embedded_record, 'checking to make sure the name is present')
        self.assertTrue(snippet_code in embedded_record, 'checking to make sure the name is present')
        for tag in snippet_tags:
            self.assertTrue(tag in embedded_record, 'checking to make sure the tags are present')
        
        
        