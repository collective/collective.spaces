from five import grok
from zope import schema
from plone.dexterity.content import Container
from plone.app.dexterity.interfaces import isValidId
from plone.directives import form
from plone.namedfile.field import NamedImage
from Products.GenericSetup.interfaces import IDAVAware

from collective.spaces import _


class ISpace(form.Schema):
    """Virtual collaboration workspace that acts as a navigation root.
    """

    form.order_before(id='*')
    id = schema.ASCIILine(
        title=_(u"Short Name"),
        description=_(u"Should not contain spaces, underscores or mixed case. "
                      u"Short Name is part of the item's web address."),
        required=False,
        constraint=isValidId
    )

    custom_logo = NamedImage(
        title=_(u"Custom Logo"),
        description=_(u"Upload a custom logo to use for your Space."),
        required=False,
    )


class Space(Container):
    grok.implements(IDAVAware)
