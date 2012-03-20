import unittest2 as unittest
from collective.spaces.testing import\
    COLLECTIVE_SPACES_INTEGRATION_TESTING


class TestBrowserViews(unittest.TestCase):
    """ Test various browser views used in this package.
    """

    layer = COLLECTIVE_SPACES_INTEGRATION_TESTING

    def setUp(self):
        """ Perform set up boilerplate functionality.
        """
        self.app = self.layer['app']
        self.portal = self.layer['portal']

