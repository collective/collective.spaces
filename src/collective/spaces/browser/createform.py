from five import grok
from zope import interface, schema
from z3c.form import button, validator

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.dexterity.interfaces import isValidId
from plone.directives import form
from plone.formwidget.recaptcha import ReCaptchaValidator

from collective.spaces import _

ALL_ROLES = ['Contributor', 'Editor', 'Reader', 'Reviewer', 'Owner']

class ICreateSpace(form.Schema):
    """Schema for through-the-web `Create a Space` form.
    """

    id = schema.TextLine(
        title=_(u"Space ID"),
        description=_(u"Select a short identifier to be part of the URL. \
                      For example, \"my-space\"; lower case, alphanumeric \
                      and dot, dash, and underscore characters only."),
        required=True,
        constraint=isValidId,
    )

    space_title = schema.TextLine(
        title=_(u"Space Title"),
        description=_(u"Textual title, which can be any characters \
                      you'd like. For example, \"North QLD Collaborators \
                      (Australia)\"."),
        required=True,
    )

    form.write_permission(template_id='collective.spaces.AddSpace')
    template_id = schema.TextLine(
        title=_(u"Template ID"),
        description=_(u"Specify the ID of the template in the portal \
                      root. By default, we should have a 'space-template' \
                      available but you can pick another. This option \
                      is only available to site administrators."),
        required=True,
        default=u"space-template",
    )

#    form.widget(captcha='plone.formwidget.recaptcha.ReCaptchaFieldWidget')
#    captcha = schema.TextLine(
#        title=_(u"Verification"),
#        description=_(u"Enter the words you see to verify your request."),
#        required=False,
#    )

class CreateSpaceForm(form.SchemaForm):
    """Form used to create Space content via the web. This form
    copies a template in order to produce a new Space. This gives the
    end administrators flexibility on the pre-canned content they provide.
    """
    grok.name('create-space')
    grok.require('collective.spaces.CreateSpaceViaWeb')
    grok.context(ISiteRoot)

    schema = ICreateSpace
    ignoreContext = True

    label = _(u"Create a new Space")
    description = _(u"Create a new collaborative Space by providing your \
                    details. Your Space will automatically be provisioned \
                    with you as the Space administrator.")

    def update(self):
        self.request.set('disable_border', True)
        super(CreateSpaceForm, self).update()

    @button.buttonAndHandler(_(u'Create'))
    def handleApply(self, action):
        """Handle the process of creating the user's new Space at the site
        root."""
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        space_id = str(data['id'])
        space_title = str(data['space_title'])
        template_id = str(data['template_id'])
        try:
            template_cp = self.context.manage_copyObjects(template_id)
            #Result looks like [{'new_id': 'copy_of_space-template', 'id': 'space-template'}]
            result = self.context.manage_pasteObjects(template_cp)
            new_space = self.context[result[0]['new_id']]
            new_space.setId(space_id)
            new_space.setTitle(space_title)

            membership_tool = getToolByName(self.context, 'portal_membership')
            member = membership_tool.getAuthenticatedMember()
            new_space.manage_setLocalRoles(member.getUserName(), ALL_ROLES)
            new_space.reindexObject()

            #If okay, then redirect to the new Space
            IStatusMessage(self.request).addStatusMessage(
                _(u"Welcome to your new Space! Start adding content and sharing \
                    with others."),
                "info"
            )

            space_url = new_space.absolute_url()
            self.request.response.redirect(space_url)
        except:
            raise
            self.status = _(u"An error occurred whilst creating your Space \
                            with this ID. Please try again or contact your \
                            site administrator if issues persist.")
            return


    @button.buttonAndHandler(_(u"Cancel"))
    def handleCancel(self, action):
        """Upon cancellation, redirect the user back to portal root.
        """
        self.request.response.redirect(self.context.absolute_url())


#Validators for form fields
class SpaceIdValidator(validator.SimpleFieldValidator):
    """Validate the space ID field."""

    def validate(self, value):
        super(SpaceIdValidator, self).validate(value)
        if value in self.context:
            raise interface.Invalid(_(u"This ID is reserved. \
                                      Please enter another."))

validator.WidgetValidatorDiscriminators(
    SpaceIdValidator,
    field=ICreateSpace['id'],
    view=CreateSpaceForm
)
grok.global_adapter(SpaceIdValidator)

class TemplateIdValidator(validator.SimpleFieldValidator):
    """Validate the template ID field."""

    def validate(self, value):
        super(TemplateIdValidator, self).validate(value)
        if value not in self.context:
            raise interface.Invalid(_(u"An object of this ID does not exist."))

validator.WidgetValidatorDiscriminators(
    TemplateIdValidator,
    field=ICreateSpace['template_id'],
    view=CreateSpaceForm
)
grok.global_adapter(TemplateIdValidator)

class SpaceReCaptchaValidator(ReCaptchaValidator):
    pass

#validator.WidgetValidatorDiscriminators(
#    SpaceReCaptchaValidator,
#    field=ICreateSpace['captcha'],
#    view=CreateSpaceForm
#)
#grok.global_adapter(SpaceReCaptchaValidator)
