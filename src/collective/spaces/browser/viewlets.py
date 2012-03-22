from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

from collective.spaces.space import ISpace

CUSTOM_LOGO_FIELD = 'custom_logo'

class CustomLogoViewlet(common.LogoViewlet):

    def update(self):
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

    Here's a simple PNG logo to use as the Space's custom logo. This is just
    a 1x1 black PNG. Set this up as the logo.

        >>> from plone import namedfile

        >>> logo = "\\x89PNG\\r\\n\\x1a\\n\\x00\\x00\\x00\\rIHDR\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x01\\x08\\x02\\x00\\x00\\x00\\x90wS\\xde\\x00\\x00\\x00\\x01sRGB\\x00\\xae\\xce\\x1c\\xe9\\x00\\x00\\x00\\x0cIDAT\\x08\\xd7c```\\x00\\x00\\x00\\x04\\x00\\x01'4'\\n\\x00\\x00\\x00\\x00IEND\\xaeB`\\x82"
        >>> space.custom_logo = namedfile.NamedImage(logo, filename=u"1x1.png")
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
        super(common.LogoViewlet, self).update()

        navigation_root = self.portal_state.navigation_root()
        self.useCustomLogo = ISpace.providedBy(navigation_root) and \
                getattr(navigation_root, CUSTOM_LOGO_FIELD)

        Viewlet = self.useCustomLogo and CustomLogoViewlet or common.LogoViewlet
        logo_viewlet = Viewlet(self.context,
                               self.request,
                               self.view,
                               self.manager)
        logo_viewlet.update()
        self.logo = logo_viewlet.render()
