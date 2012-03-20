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
