from five import grok
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


class PloneAppImagingScalesVocabulary(object):
    """Obtains available scales from plone.app.imaging.
    From collective.contentleadimage.
    """

    def __call__(self, context):
        #importing here should prevent from erros when using w/o
        #plone.app.imaging
        from plone.app.imaging.utils import getAllowedSizes
        terms = []
        sorted_scales = sorted(getAllowedSizes().iteritems(),
                              cmp=lambda x, y: cmp(x[1][0], y[1][0]),
                              reverse=True)
        for scale, (width, height) in sorted_scales:
            terms.append(SimpleTerm(value=scale,
                                    token=scale,
                                    title="%s (%dx%d)" % (scale.title(),
                                                          width,
                                                          height)
                                   )
                        )

        return SimpleVocabulary(terms)

grok.global_utility(PloneAppImagingScalesVocabulary,
                    provides=IVocabularyFactory,
                    name='collective.spaces.scales_vocabulary')
