from five import grok
from plone.dexterity.content import Container
from Products.GenericSetup.interfaces import IDAVAware


class Space(Container):
    grok.implements(IDAVAware)
