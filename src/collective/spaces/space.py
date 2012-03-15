from zope import schema
from plone.app.dexterity.interfaces import isValidId
from plone.directives import form
from plone.namedfile.field import NamedImage

from collective.spaces import _


class ISpace(form.Schema):
    """Virtual collaboration workspace that acts as a navigation root.
    """

    form.order_before(id='*')
    id = schema.ASCIILine(
        title=_(u"Short Name"),
        description=_(u"Should not contain spaces, underscores or mixed case. "
                      "Short Name is part of the item's web address."),
        required=False,
        constraint=isValidId
    )

    custom_logo = NamedImage(
        title=_(u"Custom Logo"),
        description=_(u"Upload a custom logo to use for your Space."),
        required=False,
    )


