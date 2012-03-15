from plone.directives import dexterity, form
from plone.namedfile.field import NamedImage

from collective.spaces import _


class ISpace(form.Schema):
    """Virtual collaboration workspace that acts as a navigation root.
    """

    custom_logo = NamedImage(
        title=_(u"Custom Logo"),
        description=_(u"Upload a custom logo to use for your Space."),
        required=False,
    )


