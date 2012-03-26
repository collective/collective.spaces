import unittest2 as unittest

from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

from collective.spaces.testing import\
    COLLECTIVE_SPACES_INTEGRATION_TESTING


class TestVocabulary(unittest.TestCase):

    layer = COLLECTIVE_SPACES_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

    def test_scales_vocabulary(self):
        """ Test that the plone.app.imaging image scales vocabulary works.
        """
        from zope.schema.vocabulary import SimpleVocabulary
        scales_vocabulary = queryUtility(
            IVocabularyFactory,
            name='collective.spaces.scales_vocabulary')

        vocabulary = scales_vocabulary(self.portal)
        self.assertIsInstance(vocabulary, SimpleVocabulary)

        vocabulary_titles = [x.title for x in vocabulary]
        self.assertEqual(vocabulary_titles[0], 'Large (768x768)')
        self.assertEqual(vocabulary_titles[-1], 'Listing (16x16)')
