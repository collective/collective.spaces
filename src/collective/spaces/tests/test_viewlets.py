import unittest2 as unittest
import doctest
import transaction

import zope
from z3c.form.interfaces import IValidator
from plone.app.dexterity.interfaces import InvalidIdError
from plone.testing import layered
from plone.testing.z2 import Browser
from plone.app.testing import setRoles, \
        TEST_USER_ID, TEST_USER_PASSWORD

from collective.spaces.testing import COLLECTIVE_SPACES_FUNCTIONAL_TESTING, \
        DOC_TEST_OPTIONS


def _setUp(test):
    layer = test.globs['layer']
    portal = layer['portal']
    setRoles(portal, TEST_USER_ID, ['Manager'])
    portal.invokeFactory('collective.spaces.space',
                         id='test-space',
                         title='My wonderful Space')
    layer['space'] = portal['test-space']
    portal.invokeFactory('collective.spaces.space',
                         id='test-space-2',
                         title='Another Space')
    setRoles(portal, TEST_USER_ID, ['Member'])
    transaction.commit()


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocTestSuite('collective.spaces.browser.viewlets',
                                 optionflags=DOC_TEST_OPTIONS,
                                 setUp=_setUp),
            layer=COLLECTIVE_SPACES_FUNCTIONAL_TESTING
        ),
    ])
    return suite
