'''
Created on Mar 24, 2018

@author: jdk60
'''
from model import constants
from json import JSONEncoder

class Code_Snippet_Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class Code_Snippet:
    '''
    classdocs
    '''
    def __init__(self, message, needs_approval=True):
        '''
        Constructor
        '''
        if not isinstance(message, dict):
            raise ValueError('message must be a dictionary')
        
        keys = message.keys()
        if not constants.MSG_NAME in keys:
            raise KeyError(constants.MISSING_KEY + ': %s' % constants.MSG_NAME)
        if not constants.MSG_DESC in keys:
            raise KeyError(constants.MISSING_KEY + ': %s' % constants.MSG_DESC)
        if not constants.MSG_CODE in keys:
            raise KeyError(constants.MISSING_KEY + ': %s' % constants.MSG_CODE)
        if not constants.MSG_TAGS in keys:
            raise KeyError(constants.MISSING_KEY + ': %s' % constants.MSG_TAGS)
        
        self._name = message[constants.MSG_NAME]
        self._description = message[constants.MSG_DESC]
        self._code = message[constants.MSG_CODE]
        self._tags = message[constants.MSG_TAGS]
        self._user_name = message[constants.MSG_USER_NAME]
        
        if needs_approval:
            self._tags.append(constants.MSG_NEEDS_APPROVAL)   
    
    def get_name(self):
        return self._name
    
    def get_user_name(self):
        return self._user_name
    
    def get_description(self):
        return self._description
    
    def get_code(self):
        return self._code
    
    def get_tags(self):
        return self._tags
    
    def add_tag(self, tag):
        if tag not in self._tags:
            self._tags.append(tag)
        else:
            raise ValueError('Tag already exists')
    
    def remove_tag(self, tag):
        if tag in self._tags:
            self._tags.remove(tag)
        else:
            raise ValueError('Tag not found: %s' % tag)
        
                  
