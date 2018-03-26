'''
Created on Mar 24, 2018

@author: jdk60
'''
from model import constants

class Code_Snippet:
    '''
    classdocs
    '''
    def __init__(self, message):
        '''
        Constructor
        '''
        keys = message.keys()
        if not constants.MSG_ID in keys:
            raise KeyError(constants.MISSING_ID)
        if not constants.MSG_NAME in keys:
            raise KeyError(constants.MISSING_KEY + ': %s' % constants.MSG_NAME)
        if not constants.MSG_DESC in keys:
            raise KeyError(constants.MISSING_KEY + ': %s' % constants.MSG_DESC)
        if not constants.MSG_CODE in keys:
            raise KeyError(constants.MISSING_KEY + ': %s' % constants.MSG_CODE)
        if not constants.MSG_TAGS in keys:
            raise KeyError(constants.MISSING_KEY + ': %s' % constants.MSG_TAGS)
        
        self._id = message[constants.MSG_ID]
        self._name = message[constants.MSG_NAME]
        self._description = message[constants.MSG_DESC]
        self._code = message[constants.MSG_CODE]
        self._tags = message[constants.MSG_TAGS]
        self._tags.append(constants.MSG_NEEDS_APPROVAL)
        self.print_info()
        
    def print_info(self):
        print('Name: %s' % self._name)
        print('Description: %s' % self._description)
        print('Code: %s' % self._code)
        for tag in self._tags:
            print('tag: %s' % tag)
        
                  
