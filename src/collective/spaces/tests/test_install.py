import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from collective.spaces.testing import\
    COLLECTIVE_SPACES_INTEGRATION_TESTING


class TestInstall(unittest.TestCase):

    layer = COLLECTIVE_SPACES_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_is_installed(self):
        """ Validate that our product's GS profile has been run and the product
            installed
        """
        pid = 'collective.spaces'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')

    def test_permissions_installed(self):
        """ Ensure permissions are available and set correctly.
        """
        try:
            self.portal.rolesOfPermission('collective.spaces: Add Space')
            self.portal.rolesOfPermission('collective.spaces: Create Space via web')
        except:
            self.fail('Permissions not available')

    def test_structure_created(self):
        from collective.spaces.space import ISpace

        self.assertIn('space-template', self.portal)
        self.assertTrue(ISpace.providedBy(self.portal['space-template']))