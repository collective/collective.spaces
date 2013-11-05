from five import grok
from plone.dexterity.content import Container
from Products.GenericSetup.interfaces import IDAVAware
from plone.app.dexterity.behaviors.constrains import ConstrainTypesBehavior


class Space(Container):
    grok.implements(IDAVAware)

    #Fixes for AT-based content inside a Dexterity container
    def getLocallyAllowedTypes(self, context=None):
        behavior = ConstrainTypesBehavior(self)
        return behavior.getLocallyAllowedTypes(context)

    def getImmediatelyAddableTypes(self, context=None):
        behavior = ConstrainTypesBehavior(self)
        return behavior.getImmediatelyAddableTypes(context)
