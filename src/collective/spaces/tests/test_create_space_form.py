import unittest2 as unittest
import transaction

import zope
from z3c.form.interfaces import IValidator
from plone.app.dexterity.interfaces import InvalidIdError
from plone.testing.z2 import Browser
from plone.app.testing import setRoles, \
        TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD

from collective.spaces.browser.createform import ICreateSpace
from collective.spaces.testing import COLLECTIVE_SPACES_FUNCTIONAL_TESTING

class TestCreateSpaceForm(unittest.TestCase):
    """ Test the `Create a Space` form.
    """

    layer = COLLECTIVE_SPACES_FUNCTIONAL_TESTING

    def setUp(self):
        """ Perform set up boilerplate functionality.
        """
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', id='example-page', title='Example')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        transaction.commit()

    def test_createform(self):
        """ Ensure the Create a Space form is traversable.
        """
        try:
            self.portal.restrictedTraverse('@@create-space')
        except:
            self.fail('No create form available')

    def test_createform_administrators(self):
        """ Test create Space form for types of admin users.
        """
        ROLES = ['Site Administrator', 'Manager']
        for role in ROLES:
            self._test_createform_administrators(role)

    def _test_createform_administrators(self, role):
        """ Helper method to test creation form elements as admin user.
        """
        browser = Browser(self.app)
        setRoles(self.portal, TEST_USER_ID, [role])
        transaction.commit()
        browser.addHeader('Authorization',
                          'Basic %s:%s' % (TEST_USER_NAME,
                                           TEST_USER_PASSWORD))

        browser.open(self.portal_url+'/@@create-space')
        self.assertIn('Create a new Space', browser.contents)
        self.assertIn('Template ID', browser.contents)
        try:
            browser.getControl(name='form.widgets.template_id')
        except:
            self.fail()

    def test_createform_regular_users(self):
        """ Test create Space form for types of regular (non-admin) users.
        """
        ROLES = ['Authenticated', 'Contributor']
        for role in ROLES:
            self._test_createform_regular_users(role)


    def _test_createform_regular_users(self, role):
        """ Helper method to test creation form elements as normal user.
        """
        browser = Browser(self.app)
        setRoles(self.portal, TEST_USER_ID, [role])
        transaction.commit()
        browser.addHeader('Authorization',
                          'Basic %s:%s' % (TEST_USER_NAME,
                                           TEST_USER_PASSWORD))

        browser.open(self.portal_url+'/@@create-space')
        self.assertIn('Create a new Space', browser.contents)
        self.assertNotIn('Template ID', browser.contents)
        self.assertRaises(LookupError,
                          browser.getControl,
                          name='form.widgets.template_id')

    def test_createform_anonymous(self):
        """ Ensure logged out users cannot access creation form.
        """
        browser = Browser(self.app)
        browser.open(self.portal_url + '/logout')

        browser.open(self.portal_url+'/@@create-space')
        self.assertNotIn('Create a new Space', browser.contents)

    def test_space_id_validator(self):
        """ Test Space ID validator to check characters and ID doesn't exist.
        """
        validator = zope.component.queryMultiAdapter((self.portal,
                                                      None,
                                                      None,
                                                      ICreateSpace['id'],
                                                      None), IValidator)

        self.assertRaises(InvalidIdError, validator.validate, u'example!')
        self.assertRaises(InvalidIdError, validator.validate, u'example@')
        self.assertRaises(InvalidIdError, validator.validate, u'example#')

        #Check the existance of this ID
        self.assertIn('space-template', self.portal)
        #Should deny validation
        self.assertRaisesRegexp(zope.interface.Invalid, 'ID is reserved',
                                validator.validate, u'space-template')


        self.assertIsNone(validator.validate(u'a-valid-id'))
        self.assertIsNone(validator.validate(u'another_valid.id'))

    def test_template_id_validator(self):
        """ Test the Space template ID validator to check for obj existance.
        """
        validator = zope.component.queryMultiAdapter(
            (self.portal, None, None, ICreateSpace['template_id'], None),
            IValidator)

        #This doesn't exist and should fail
        self.assertNotIn('asdf', self.portal)
        self.assertRaisesRegexp(zope.interface.Invalid, 'does not exist',
                                validator.validate, u'asdf')

        #This does exist and should validate
        self.assertIn('space-template', self.portal)
        self.assertIsNone(validator.validate(u'space-template'))

        #The template ID doesn't have to be a Space - it can be anything
        self.assertIn('example-page', self.portal)
        self.assertIsNone(validator.validate(u'example-page'))

