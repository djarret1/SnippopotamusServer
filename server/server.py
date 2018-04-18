import zmq
import time
import json
import os
from model import constants
from model.code_snippet import Code_Snippet
from model.code_snippet import Code_Snippet_Encoder

'''
Server for the Snippopotamus Rex application
@author: David Jarrett
'''
class Server:
    
    '''
    Initialize the server.
    
    @param ip_port The ip and port that the server should run on
    @param users_file The location of the file containing valid usernames
    @param snippets_file The location of the file containing stored code snippet data
    '''
    def __init__(self, ip_port='tcp://127.0.0.1:5555', users_file='../server/users.txt', snippets_file='../server/snippets.txt'):
        self._users = set()
        self._code_snippets = {}
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)
        self._socket.bind(ip_port)
        
        self._user_file = users_file
        self._snippet_file = snippets_file
        
        self.load_users()
        self.load_all_snippets()

    def load_users(self):
        try:
            with open(self._user_file) as inputFile:
                for user in inputFile:
                    self._users.add(user.strip())
        except FileNotFoundError:
            with open(self._user_file, 'w') as outputFile:
                outputFile.write(constants.USR_ADMIN + '\n')
            self.load_users()

    def load_all_snippets(self):
        try:
            with open(self._snippet_file) as inputFile:
                for line in inputFile:
                    loaded_snippet = self.load_snippet(line)
                    snippet_handle = loaded_snippet.get_user_name() + loaded_snippet.get_name()
                    self._code_snippets[snippet_handle] = loaded_snippet
        except FileNotFoundError:
            #use empty _users dictionary
            pass
        except IndexError:
            return
    
    def load_snippet(self, field_string):
        fields = field_string.strip().split(',')
        build_message = {constants.MSG_USER_NAME: fields[0],
                         constants.MSG_NAME: fields[1],
                         constants.MSG_DESC: fields[2],
                         constants.MSG_CODE: fields[3],
                         constants.MSG_TAGS: []}
        for i in range(4, len(fields)):
            build_message[constants.MSG_TAGS].append(fields[i])
        return Code_Snippet(build_message, needs_approval=False)
    
    def store_snippet(self, code_snippet):
        user_name = code_snippet.get_user_name()
        snippet_name = code_snippet.get_name()
        desc = code_snippet.get_description()
        code = code_snippet.get_code()
        tags = code_snippet.get_tags()
        
        output_line = '%s,%s,%s,%s,' % (user_name, snippet_name, desc, code)
        for tag in tags:
            output_line += tag + ','
        output_line = output_line.rstrip(',')
               
        with open(self._snippet_file, 'a') as outputFile:
            outputFile.write(output_line + '\n')
    
    def store_all_snippets(self):
        os.remove(self._snippet_file)
        for k, v in self._code_snippets.items():
            self.store_snippet(v)
    
    '''
    Starts the main processing loop of the server. Waits for incoming commands and processes them, in turn.
    Can only be terminated by sending the TERMINATE command to the server.
    
    @preconditions: None
    @postconditions: Any changes due to processing commands will be reflected.
    '''    
    def main_loop(self):
        result = ''
        while result != constants.COMMAND_TERMINATE:
            #  Wait for next request from client
            print("waiting for message...")
            json_message = self._socket.recv_string()
            #print('********' + json_message + '*********')
            message = json.loads(json_message)
            try:
                print("Received request: %s" % message[constants.MSG_ID])
                print("From: %s" % message[constants.MSG_USER_NAME])
            
                if not self.validate_user(message) and message[constants.MSG_ID] != constants.COMMAND_NEW_USER:
                    self.send_response(constants.INVALID_USER)
                else:
                    result = self.process_message(message)
            except KeyError as e:
                self.send_response(constants.MISSING_KEY + ': ' + str(e))
        
    def process_message(self, message):
        try:
            response = self.dispatch_message(message)
            json_message = json.dumps(response)
            if response != None:
                self._socket.send_string(json_message)
            return response
        except KeyError as e:
            self.send_response(str(e))
            return response

    def dispatch_message(self, message):
        try:
            if message[constants.MSG_ID] == constants.COMMAND_DUMP:
                return self.dump_all_snippets(message)
            if message[constants.MSG_ID] == constants.COMMAND_ADD:
                return self.add_snippet(message)
            if message[constants.MSG_ID] == constants.COMMAND_DELETE:
                return self.delete_snippet(message)
            if message[constants.MSG_ID] == constants.COMMAND_DELETE_ALL:
                return self.delete_all_snippets()
            if message[constants.MSG_ID] == constants.COMMAND_NEW_USER:
                return self.add_user(message)
            if message[constants.MSG_ID] == constants.COMMAND_UPDATE:
                return self.update_snippet(message)
            if message[constants.MSG_ID] == constants.COMMAND_TERMINATE:
                return constants.COMMAND_TERMINATE
            return self.send_response(constants.UNKNOWN_ID + ': ' + message[constants.MSG_ID])
        except KeyError as e:
            return self.send_response(constants.MISSING_KEY + ': ' + str(e))
        except Exception as e:
            return self.send_response(str(e))

    def add_snippet(self, message):
        new_snippet = Code_Snippet(message)
        snippet_handle = new_snippet.get_user_name() + new_snippet.get_name() 
        if (snippet_handle) in self._code_snippets.keys():
            return {constants.RESPONSE: constants.SNIPPET_EXISTS}
        self._code_snippets[snippet_handle] = new_snippet
        self.store_snippet(new_snippet)
        return {constants.RESPONSE: constants.SUCCESS}

    def add_user(self, message):
        if message[constants.MSG_USER_NAME] in self._users:
            return {constants.RESPONSE: constants.USER_EXISTS}
        self._users.add(message[constants.MSG_USER_NAME])
        with open(self._user_file, 'a') as output_file:
            output_file.write(message[constants.MSG_USER_NAME] + '\n')
            return {constants.RESPONSE: constants.SUCCESS}

    def update_snippet(self, message):
        new_snippet = Code_Snippet(message, False)
        snippet_handle = new_snippet.get_user_name() + new_snippet.get_name() 
        if (snippet_handle) not in self._code_snippets.keys():
            return {constants.RESPONSE: constants.SNIPPET_DOESNT_EXIT}
        self._code_snippets[snippet_handle] = new_snippet
        self.store_all_snippets()
        return {constants.RESPONSE: constants.SUCCESS}
    
    def delete_snippet(self, message):
        new_snippet = Code_Snippet(message, False)
        snippet_handle = new_snippet.get_user_name() + new_snippet.get_name() 
        if (snippet_handle) not in self._code_snippets.keys():
            return {constants.RESPONSE: constants.SNIPPET_DOESNT_EXIT}
        del self._code_snippets[snippet_handle]
        self.store_all_snippets()
        return {constants.RESPONSE: constants.SUCCESS}
    
    def delete_all_snippets(self):
        open('snippets.txt', 'w').close()
        self._code_snippets = {}
        return {constants.RESPONSE: constants.SUCCESS}
    
    def send_response(self, text):
        response = json.dumps( {constants.RESPONSE: text} )
        self._socket.send_string(response)

    def validate_user(self, message):
        if message[constants.MSG_USER_NAME] in self._users:
            return True
        return False
        
    def dump_all_snippets(self, message):
        file_string = ''
        with open('snippets.txt', 'r') as snippet_file:
            for line in snippet_file:
                message[constants.MSG_USER_NAME]
                if message[constants.MSG_USER_NAME] != constants.USR_ADMIN and 'needs_approval' not in line:
                    file_string += line
                elif message[constants.MSG_USER_NAME] == constants.USR_ADMIN:
                    file_string += line
            
        return {constants.RESPONSE: file_string}
                        
#         result = {}
#         count = 0
#         for k, v in self._code_snippets.items():
#             result[count] = v
#             count = count + 1
#         all_snippets = json.dumps(result, cls=Code_Snippet_Encoder)
#         return {constants.RESPONSE: all_snippets}

'''
Starts the server on the main thread.
@preconditions: None
@postconditions: Server will be running on main thread.
'''
def runServer():
    server = Server()
    server.main_loop()

if(__name__ == "__main__"):
    runServer()
