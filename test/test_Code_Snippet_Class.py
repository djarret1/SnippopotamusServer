'''
Created on Mar 26, 2018

@author: jdk60
'''
import unittest
from model.code_snippet import Code_Snippet
import model.constants as constants
from builtins import ValueError

class Test(unittest.TestCase):

    def testWhenCodeSnippetCreatedWithAllRequiredKeysWithDefaultApprovalLevel(self):
        test_user = 'test_user'
        test_snippet = 'test_snippet'
        test_description = 'test_description'
        test_code = 'test_code'
        test_tags = ['tag1', 'tag2']
        
        message = {constants.MSG_USER_NAME: test_user,
                   constants.MSG_NAME: test_snippet,
                   constants.MSG_DESC: test_description,
                   constants.MSG_CODE: test_code,
                   constants.MSG_TAGS: test_tags}
        
        snippet = Code_Snippet(message)
        self.assertEqual(test_user, snippet.get_user_name(), "checking user-name was set")
        self.assertEqual(test_snippet, snippet.get_name(), "checking name of snippet was set")
        self.assertEqual(test_description, snippet.get_description(), "checking description was set")
        self.assertEqual(test_code, snippet.get_code(), "checking code was set")
        self.assertEqual(test_tags, snippet.get_tags(), "checking tags were set")
        self.assertTrue(constants.MSG_NEEDS_APPROVAL in snippet.get_tags(), "making sure default approval level is true")
    
    def testWhenCodeSnippetCreatedWithAllRequiredKeysWithApprovalNotRequired(self):
        test_user = 'test_user'
        test_snippet = 'test_snippet'
        test_description = 'test_description'
        test_code = 'test_code'
        test_tags = ['tag1', 'tag2']
        
        message = {constants.MSG_USER_NAME: test_user,
                   constants.MSG_NAME: test_snippet,
                   constants.MSG_DESC: test_description,
                   constants.MSG_CODE: test_code,
                   constants.MSG_TAGS: test_tags}
        
        snippet = Code_Snippet(message, needs_approval=False)
        self.assertEqual(test_user, snippet.get_user_name(), "checking user-name was set")
        self.assertEqual(test_snippet, snippet.get_name(), "checking name of snippet was set")
        self.assertEqual(test_description, snippet.get_description(), "checking description was set")
        self.assertEqual(test_code, snippet.get_code(), "checking code was set")
        self.assertEqual(test_tags, snippet.get_tags(), "checking tags were set")
        self.assertFalse(constants.MSG_NEEDS_APPROVAL in snippet.get_tags(), "making sure default approval level is true")
        
    def testWhenCodeSnippetCreatedWithMissingSnippetName(self):
        test_user = 'test_user'
        test_description = 'test_description'
        test_code = 'test_code'
        test_tags = ['tag1', 'tag2']
        
        message = {constants.MSG_USER_NAME: test_user,
                   constants.MSG_DESC: test_description,
                   constants.MSG_CODE: test_code,
                   constants.MSG_TAGS: test_tags}
        
        with self.assertRaises(KeyError):
            Code_Snippet(message)
            
    def testWhenCodeSnippetCreatedWithMissingUserName(self):
        test_snippet = 'test_snippet'
        test_description = 'test_description'
        test_code = 'test_code'
        test_tags = ['tag1', 'tag2']
        
        message = {constants.MSG_NAME: test_snippet,
                   constants.MSG_DESC: test_description,
                   constants.MSG_CODE: test_code,
                   constants.MSG_TAGS: test_tags}
        
        with self.assertRaises(KeyError):
            Code_Snippet(message)
            
    def testWhenCodeSnippetCreatedWithMissingDescription(self):
        test_user = 'test_user'
        test_snippet = 'test_snippet'
        test_code = 'test_code'
        test_tags = ['tag1', 'tag2']
        
        message = {constants.MSG_USER_NAME: test_user,
                   constants.MSG_NAME: test_snippet,
                   constants.MSG_CODE: test_code,
                   constants.MSG_TAGS: test_tags}
        
        with self.assertRaises(KeyError):
            Code_Snippet(message)
            
    def testWhenCodeSnippetCreatedWithMissingCode(self):
        test_user = 'test_user'
        test_snippet = 'test_snippet'
        test_description = 'test_description'
        test_tags = ['tag1', 'tag2']
        
        message = {constants.MSG_USER_NAME: test_user,
                   constants.MSG_NAME: test_snippet,
                   constants.MSG_DESC: test_description,
                   constants.MSG_TAGS: test_tags}
        
        with self.assertRaises(KeyError):
            Code_Snippet(message)
            
    def testWhenCodeSnippetCreatedWithMissingTags(self):
        test_user = 'test_user'
        test_snippet = 'test_snippet'
        test_description = 'test_description'
        test_code = 'test_code'
        
        message = {constants.MSG_USER_NAME: test_user,
                   constants.MSG_NAME: test_snippet,
                   constants.MSG_DESC: test_description,
                   constants.MSG_CODE: test_code}
        
        with self.assertRaises(KeyError):
            Code_Snippet(message)
        
    def testWhenCodeSnippetCreatedWithEmptyTags(self):
        test_user = 'test_user'
        test_snippet = 'test_snippet'
        test_description = 'test_description'
        test_code = 'test_code'
        test_tags = []
        
        message = {constants.MSG_USER_NAME: test_user,
                   constants.MSG_NAME: test_snippet,
                   constants.MSG_DESC: test_description,
                   constants.MSG_CODE: test_code,
                   constants.MSG_TAGS: test_tags}
        
        snippet = Code_Snippet(message)
        self.assertTrue(1, len(snippet.get_tags()))
        
    def testWhenAddTagToSnippet(self):
        test_user = 'test_user'
        test_snippet = 'test_snippet'
        test_description = 'test_description'
        test_code = 'test_code'
        test_tags = []
        
        message = {constants.MSG_USER_NAME: test_user,
                   constants.MSG_NAME: test_snippet,
                   constants.MSG_DESC: test_description,
                   constants.MSG_CODE: test_code,
                   constants.MSG_TAGS: test_tags}
        
        snippet = Code_Snippet(message)
        self.assertTrue(1 == len(snippet.get_tags()), 'checking that only the default tag is present')
        
        test_tag = 'TEST_TAG'
        snippet.add_tag(test_tag)
        self.assertTrue(test_tag in snippet.get_tags(), 'checking that the new tag was added')
        
    def testWhenAddExistingTagToSnippet(self):
        test_user = 'test_user'
        test_snippet = 'test_snippet'
        test_description = 'test_description'
        test_code = 'test_code'
        test_tags = []
        
        message = {constants.MSG_USER_NAME: test_user,
                   constants.MSG_NAME: test_snippet,
                   constants.MSG_DESC: test_description,
                   constants.MSG_CODE: test_code,
                   constants.MSG_TAGS: test_tags}
        
        snippet = Code_Snippet(message)
        self.assertTrue(constants.MSG_NEEDS_APPROVAL in snippet.get_tags(), 'checking that the default tag is present')
        
        with self.assertRaises(ValueError):
            snippet.add_tag(constants.MSG_NEEDS_APPROVAL)
        
    def testWhenRemoveTagFromSnippet(self):
        test_user = 'test_user'
        test_snippet = 'test_snippet'
        test_description = 'test_description'
        test_code = 'test_code'
        test_tag = 'test_tag'
        test_tags = [test_tag]
        
        message = {constants.MSG_USER_NAME: test_user,
                   constants.MSG_NAME: test_snippet,
                   constants.MSG_DESC: test_description,
                   constants.MSG_CODE: test_code,
                   constants.MSG_TAGS: test_tags}
        
        snippet = Code_Snippet(message)
        self.assertTrue(test_tag in snippet.get_tags(), 'checking that the test tag is present')
        
        snippet.remove_tag(test_tag)
        self.assertFalse(test_tag in snippet.get_tags(), 'checking that the test tag was removed')
        
    def testWhenRemoveNonExistentTagFromSnippet(self):
        test_user = 'test_user'
        test_snippet = 'test_snippet'
        test_description = 'test_description'
        test_code = 'test_code'
        test_tags = []
        
        message = {constants.MSG_USER_NAME: test_user,
                   constants.MSG_NAME: test_snippet,
                   constants.MSG_DESC: test_description,
                   constants.MSG_CODE: test_code,
                   constants.MSG_TAGS: test_tags}
        
        snippet = Code_Snippet(message)
        self.assertTrue(1 == len(snippet.get_tags()), 'checking that the default tag is present')
        
        with self.assertRaises(ValueError):
            snippet.remove_tag('THIS TAG DOES NOT EXIST')
            
    def testWhenTryToConstructWithNonDictionary(self):
        with self.assertRaises(ValueError):
            Code_Snippet('a string')
        
        