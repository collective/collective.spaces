import unittest2 as unittest

from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

from collective.spaces.testing import\
    COLLECTIVE_SPACES_INTEGRATION_TESTING

from collective.spaces import utils


class TestUtils(unittest.TestCase):

    layer = COLLECTIVE_SPACES_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

    def test_elevated_access_restores_sm(self):
        """ Test evalated_access util restores a SecurityManager on exception.
        """
        class DummySecurityPolicy(object):
            """ Dummy security policy to deny all permissions."""

            def checkPermission(self, permission, object):
                """ Deny any permissions."""
                return False

        from zope.security._definitions import thread_local
        thread_local.interaction = DummySecurityPolicy()

        @utils.elevated_access
        def fn(context):
            raise TypeError('elevated_access')

        #Ensure our error gets raised but SM gets restored
        from AccessControl.SecurityManagement import getSecurityManager
        before_sm = getSecurityManager()
        self.assertRaisesRegexp(TypeError, 'elevated_access', fn, self.portal)
        after_sm = getSecurityManager()

        self.assertEqual(before_sm, after_sm)
