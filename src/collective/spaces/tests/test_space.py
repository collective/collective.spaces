import unittest2 as unittest

from zope.component import queryUtility

from Products.CMFCore.utils import getToolByName
from plone.dexterity.interfaces import IDexterityFTI

from collective.spaces.testing import\
    COLLECTIVE_SPACES_INTEGRATION_TESTING


class TestSpace(unittest.TestCase):

    layer = COLLECTIVE_SPACES_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

    def test_fti_available(self):
        """ Validate that our Dexterity FTI is available
        """
        fti = queryUtility(IDexterityFTI, name='collective.spaces.space')
        self.assertIsNotNone(fti)

    def test_schema(self):
        from collective.spaces.interfaces import ISpace

        fti = queryUtility(IDexterityFTI, name='collective.spaces.space')
        schema = fti.lookupSchema()
        self.assertEqual(ISpace, schema)

    def test_factory(self):
        from zope.component import createObject
        from collective.spaces.interfaces import ISpace
        fti = queryUtility(IDexterityFTI, name='collective.spaces.space')
        ISpace.providedBy(createObject(fti.factory))

    def test_fti_views(self):
        fti = queryUtility(IDexterityFTI, name='collective.spaces.space')

        #Should have several view methods, not just 'view'
        self.assertGreater(len(fti.view_methods), 1)
        self.assertIn('folder_listing', fti.view_methods)

    def test_creation(self):
        from plone.app.testing import login, setRoles, TEST_USER_NAME, \
                TEST_USER_ID
        from AccessControl import Unauthorized

        login(self.portal, TEST_USER_NAME)

        #Normal user (Contributor) cannot create
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        self.assertRaises(Unauthorized,
                          self.portal.invokeFactory,
                          'collective.spaces.space',
                          'my-space')

        #Site Administrator can create
        setRoles(self.portal, TEST_USER_ID, ['Site Administrator'])
        self.portal.invokeFactory('collective.spaces.space', 'space')
        self.assertIn('space', self.portal)

        #Manager can create
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('collective.spaces.space', 'space2')
        self.assertIn('space2', self.portal)

    #def test_debug(self):
    #    import ipdb; ipdb.set_trace()
