from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

from collective.spaces.interfaces import ISpace

CUSTOM_LOGO_FIELD = 'custom_logo'


class CustomLogoViewlet(common.LogoViewlet):
    """ Logo viewlet used to customise logos for Space areas.

    Users have the ability to specify their own logo against their Space
    and this viewlet will render this accordingly. This logo builds upon
    what Plone's default logo viewlet does in rendering.

    Users can also select a scale for their image. Check to make sure this
    selection is relfected correctly.

        >>> app = layer['app']
        >>> portal = layer['portal']
        >>> space = layer['space']

    Read in an image to use

        >>> import os
        >>> import collective.spaces
        >>> filename = os.path.join(
        ...     os.path.dirname(collective.spaces.__file__),
        ...     'resources',
        ...     'spaces-logo.png')
        >>> image = open(filename, 'rb').read()

    Set it as the custom Space logo

        >>> import transaction
        >>> from plone import namedfile
        >>> space.custom_logo = namedfile.NamedImage(image,
        ...                                          filename=u"img.png")
        >>> transaction.commit()

    Load up our test browser to check the custom logo

        >>> from plone.testing.z2 import Browser
        >>> browser = Browser(app)
        >>> browser.open(space.absolute_url())
        >>> '<img src="http://nohost/plone/test-space/@@images/' \\
        ...     in browser.contents
        True

    Scaling is set at 400x400 by default

        >>> 'title="My wonderful Space" height="101" width="400" /></a>' \\
        ...     in browser.contents
        True

    Change scaling and reload the page. Any of the plone.app.imaging scales
    can be selected here.

        >>> space.custom_logo_scale = "thumb"
        >>> transaction.commit()
        >>> browser.reload()

        >>> 'title="My wonderful Space" height="32" width="128" /></a>' \\
        ...     in browser.contents
        True

    Remove the custom logo

        >>> space.custom_logo = None
        >>> transaction.commit()

    """

    def update(self):
        """ Update the viewlet with suitable properties.
        """
        super(common.LogoViewlet, self).update()

        navigation_root = self.portal_state.navigation_root()
        scales = navigation_root.restrictedTraverse('@@images')
        self.logo_tag = scales.scale(
            CUSTOM_LOGO_FIELD,
            scale=navigation_root.custom_logo_scale).tag()
        self.navigation_root_title = self.portal_state.navigation_root_title()


class LogoViewlet(common.LogoViewlet):
    """ Logo viewlet used to override Plone's default logo.

    This viewlet will utilise Plone's default logo unless the current
    navigation root is a Space and has a custom logo applied to it.

        >>> import transaction
        >>> from plone.testing.z2 import Browser

        >>> app = layer['app']
        >>> portal = layer['portal']
        >>> space = layer['space']
        >>> browser = Browser(app)

    Check the default portal logo is being used in non-Space areas.

        >>> browser.open(portal.absolute_url())
        >>> browser.getLink(id='portal-logo')
        <Link text='Plone site[IMG]' ...
        >>> '<img src="http://nohost/plone/logo.png"' in browser.contents
        True

    Visit the Space and this should be the same for now.

        >>> browser.open(space.absolute_url())
        >>> browser.getLink(id='portal-logo')
        <Link text='Plone site[IMG]' ...
        >>> '<img src="http://nohost/plone/logo.png"' in browser.contents
        True

    Here's a simple PNG logo to use as the Space's custom logo.

        >>> import os
        >>> import collective.spaces
        >>> filename = os.path.join(
        ...     os.path.dirname(collective.spaces.__file__),
        ...     'resources',
        ...     'spaces-logo.png')
        >>> image = open(filename, 'rb').read()

        >>> from plone import namedfile
        >>> space.custom_logo = namedfile.NamedImage(image,
        ...                                          filename=u"1x1.png")
        >>> transaction.commit()

    Check to see this is now visible

        >>> browser.reload()
        >>> browser.getLink(id='portal-logo')
        <Link text='My wonderful Space[IMG]' url='.../test-space'>
        >>> '<img src="http://nohost/plone/test-space/@@images/' \\
        ...     in browser.contents
        True

    Sanity check to ensure this logo doesn't go and escape to anywhere else
    on the site.

        >>> browser.open(portal.absolute_url())
        >>> '<img src="http://nohost/plone/logo.png"' in browser.contents
        True

        >>> browser.open(portal['test-space-2'].absolute_url())
        >>> '<img src="http://nohost/plone/logo.png"' in browser.contents
        True

    """
    index = ViewPageTemplateFile('logo.pt')

    def update(self):
        """ Update the viewlet with suitable properties.

        This method renders the correct logo accordingly and the thin
        logo.pt file only shows this resulting HTML.
        """
        super(common.LogoViewlet, self).update()

        navigation_root = self.portal_state.navigation_root()
        self.useCustomLogo = ISpace.providedBy(navigation_root) and \
                getattr(navigation_root, CUSTOM_LOGO_FIELD)

        Viewlet = self.useCustomLogo and CustomLogoViewlet \
                or common.LogoViewlet
        logo_viewlet = Viewlet(self.context,
                               self.request,
                               self.view,
                               self.manager)
        logo_viewlet.update()
        self.logo = logo_viewlet.render()
