'''
Created on Mar 24, 2018

@author: David Jarrett
'''

'''
Messages sent to the server are sent in the form of a dictionary that has been JSON serialized.

---------Every message sent to the server must include:
 a MSG_ID key, followed by a value representing the command.
 a MSG_USER_NAME key, with a valid user-name value.
 
 The COMMAND_ADD adds a code snippet to the server (duplicates will be rejected)
 This requires the aforementioned data, as well as:
 MSG_NAME: the name of the code snippet
 MSG_DESC: its description
 MSG_CODE: the code stored in the snippet
 MSG_TAGS: a list of tags for the snippet
 
 The COMMAND_DUMP requests a full data dump from the server.
 MSG_ID: COMMAND_DUMP
 This data is in the form of a string with each snippet delimited by ascending numeric values.
 
 The COMMAND_NEW_USER adds a new user to the system.
 MSG_USER_NAME: the username to add (duplicates rejected)
 
 The COMMAND_UPDATE will update an existing snippet. It requires all of the
 same information that would be required if you were adding a new snippet.
 
 COMMAND_TERMINATE kills the server.  

'''
MSG_ID = 'id'
MSG_USER_NAME = 'user_name'
MSG_NAME = 'name'
MSG_DESC = 'description'
MSG_CODE = 'code'
MSG_TAGS = 'tags'

NEW_TAG = 'new_tag'
TAG_TO_DELETE = 'tag_to_delete'
OLD_NAME = 'old_name'

MSG_NEEDS_APPROVAL = 'needs_approval'

RESPONSE = 'resp'
SUCCESS = 'success'
MISSING_ID = 'missing_id'
UNKNOWN_ID = 'unknown_id'
MISSING_KEY = 'missing_key'
INVALID_USER = 'invalid_user'
VALID_USER = 'valid_user'
USER_EXISTS = 'user_exists'

USR_ADMIN = 'admin'
SNIPPET_EXISTS = 'snippet_exists'
SNIPPET_DOESNT_EXIT = 'snippet_doesnt_exist'

COMMAND_ADD = 'add'
COMMAND_DELETE = 'delete'
COMMAND_DELETE_ALL = 'delete_all'
COMMAND_DUMP = 'dump'
COMMAND_NEW_USER = 'new_user'
COMMAND_TERMINATE = 'terminate'
COMMAND_TAG_SNIPPET = 'tag_snippet'
COMMAND_UNTAG_SNIPPET = 'untag_snippet'
COMMAND_UPDATE = 'update'