'''
Created on Mar 24, 2018

@author: jdk60
'''
from model import constants

class code_snippet:
    '''
    classdocs
    '''
    def __init__(self, message):
        '''
        Constructor
        '''
        self._id = message[constants.MSG_ID]
        self._name = message[constants.MSG_NAME]
        self._description = message[constants.MSG_DESC]
        self._code = message[constants.MSG_CODE]
        self._tags = message[constants.MSG_TAGS]
        self.print_info()
        
    def print_info(self):
        print('Name: %s' % self._name)
        print('Description: %s' % self._description)
        print('Code: %s' % self._code)
        for tag in self._tags:
            print('tag: %s' % tag)
        
                  
