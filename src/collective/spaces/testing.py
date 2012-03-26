import doctest

from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig


class CollectiveSpaces(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import collective.spaces
        xmlconfig.file('configure.zcml',
                       collective.spaces,
                       context=configurationContext)
        xmlconfig.file('overrides.zcml',
                       collective.spaces,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.spaces:default')

COLLECTIVE_SPACES_FIXTURE = CollectiveSpaces()
COLLECTIVE_SPACES_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(COLLECTIVE_SPACES_FIXTURE, ),
                       name="CollectiveSpaces:Integration")
COLLECTIVE_SPACES_FUNCTIONAL_TESTING = \
    FunctionalTesting(bases=(COLLECTIVE_SPACES_FIXTURE, ),
                       name="CollectiveSpaces:Functional")

DOC_TEST_OPTIONS = doctest.ELLIPSIS \
        | doctest.REPORT_ONLY_FIRST_FAILURE \
        | doctest.NORMALIZE_WHITESPACE
