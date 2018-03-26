import zmq
import time
import json
from model import constants
from model.code_snippet import Code_Snippet

user_file = '../server/users.txt'
snippet_file = '../server/snippets.txt'
ip_port = "tcp://127.0.0.1:5555"

class Server:
    
    def __init__(self):
        self._users = set()
        self._code_snippets = {}
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)
        self._socket.bind(ip_port)
        
        self.load_users()
        self.load_all_snippets()

    def load_users(self):
        try:
            with open(user_file) as inputFile:
                for user in inputFile:
                    self._users.add(user.strip())
        except FileNotFoundError:
            with open(user_file, 'w') as outputFile:
                outputFile.write(constants.USR_ADMIN + '\n')
            self.load_users()

    def load_all_snippets(self):
        try:
            with open(snippet_file) as inputFile:
                for line in inputFile:
                    loaded_snippet = self.load_snippet(line)
                    snippet_handle = loaded_snippet.get_user_name() + loaded_snippet.get_name()
                    self._code_snippets[snippet_handle] = loaded_snippet
        except FileNotFoundError:
            #use empty _users dictionary
            pass
    
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
               
        try:
            with open(snippet_file, 'a') as outputFile:
                outputFile.write(output_line + '\n')
        except FileNotFoundError:
            with open(snippet_file, 'w') as outputFile:
                outputFile.write(output_line + '\n')
    
    def main_loop(self):
        result = ''
        while result != constants.COMMAND_TERMINATE:
            #  Wait for next request from client
            print("waiting for message...")
            json_message = self._socket.recv_string()
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
            self._socket.send_string(json_message)
            return response
        except KeyError as e:
            self.send_response(str(e))
            return response

    def dispatch_message(self, message):
        if message[constants.MSG_ID] == constants.COMMAND_ADD:
            return self.add_snippet(message)
        if message[constants.MSG_ID] == constants.COMMAND_NEW_USER:
            return self.add_user(message)
        if message[constants.MSG_ID] == constants.COMMAND_TERMINATE:
            return constants.COMMAND_TERMINATE
        return self.send_response(constants.UNKNOWN_ID + ': ' + message[constants.MSG_ID])

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
        with open(user_file, 'a') as output_file:
            output_file.write(message[constants.MSG_USER_NAME] + '\n')
            return {constants.RESPONSE: constants.SUCCESS}

    def send_response(self, text):
        response = json.dumps( {constants.RESPONSE: text} )
        self._socket.send_string(response)

    def validate_user(self, message):
        if message[constants.MSG_USER_NAME] in self._users:
            return True
        return False

def runServer():
    server = Server()
    server.main_loop()

if(__name__ == "__main__"):
    runServer()
