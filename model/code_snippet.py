'''
Created on Mar 24, 2018

@author: David Jarrett
'''
from model import constants
from json import JSONEncoder

'''
Required to JSON serialize Code_Snippet objects.
'''
class Code_Snippet_Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

'''
The server-side representation of a code snippet
'''
class Code_Snippet:
    
    '''
    Ensures that all required keys for the creation of the snippet are present in the message dictionary.
    By default, when the snippet is added to the server, it is tagged as needing approval. This
    can be overridden by passing False to the needs_approval parameter.
    @precondition: message IS A dictionary containing the KV pairs:
        MSG_NAME: name
        MSG_DESC: description
        MSG_CODE: the code
        MSG_TAGS: list of tags
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
    
    '''
    Returns the name of the code snippet.
    @precondition: None
    @return: The name of the code snippet.
    '''
    def get_name(self):
        return self._name
    
    '''
    Returns the user-name of the person who added this snippet.
    @precondition: None
    @return: The user-name of the person who added this snippet.
    '''
    def get_user_name(self):
        return self._user_name
    
    '''
    Returns the description of the code snippet.
    @precondition: None
    @return: The description of the code snippet.
    '''
    def get_description(self):
        return self._description
    
    '''
    Returns the code associated with the code snippet.
    @precondition: None
    @return: The code associated with the code snippet.
    '''
    def get_code(self):
        return self._code
    
    '''
    Returns the tags associated with the code snippet.
    @precondition: None
    @return: The tags associated with the code snippet.
    '''
    def get_tags(self):
        return self._tags
    
    '''
    Adds a new tag to this code snippet.
    @precondition: Tag cannot already exist in snippet
    @postcondition: Tag will be added to the snippet
    '''
    def add_tag(self, tag):
        if tag not in self._tags:
            self._tags.append(tag)
        else:
            raise ValueError('Tag already exists')
    
    '''
    Removes a tag from this code snippet.
    @precondition: Tag must exist in the snippet
    @postcondition: Tag will be removed from the snippet
    '''
    def remove_tag(self, tag):
        if tag in self._tags:
            self._tags.remove(tag)
        else:
            raise ValueError('Tag not found: %s' % tag)
        
                  