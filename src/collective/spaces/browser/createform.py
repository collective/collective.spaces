from five import grok
from zope import interface, schema
from zope.security import checkPermission
from z3c.form import button, validator

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.dexterity.interfaces import isValidId
from plone.directives import form

from collective.spaces import _, utils

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


class CreateSpaceForm(form.SchemaForm):
    """Form used to create Space content via the web.

    This form clones a template in order to produce a new Space. This gives the
    end administrators flexibility on the pre-canned content they provide.

        >>> from plone.app import testing
        >>> import transaction

        >>> app = layer['app']
        >>> portal = layer['portal']

    Initialise the testing browser and log in.

        >>> from plone.testing.z2 import Browser
        >>> browser = Browser(app)
        >>> portal_url = portal.absolute_url()
        >>> browser.open(portal_url)
        >>> browser.addHeader('Authorization',
        ...   'Basic %s:%s' % (testing.TEST_USER_NAME,
        ...                    testing.TEST_USER_PASSWORD,))

    Login as a regular user with the Authenticated role.

        >>> testing.setRoles(portal, testing.TEST_USER_ID, ['Authenticated'])
        >>> transaction.commit()
        >>> browser.reload()
        >>> testing.TEST_USER_ID in browser.contents
        True

    Load the form

        >>> browser.open(portal_url+'/@@create-space')
        >>> 'Create a new Space' in browser.contents
        True

    Enter details onto the form to create the Space

        >>> browser.getControl('Space ID').value = 'new-id'
        >>> browser.getControl('Space Title').value = \\
        ...     'Custom title'

    Ensure the Template ID field isn't present at the moment.

        >>> browser.getControl('Template ID')
        Traceback (most recent call last):
        ...
        LookupError:...

    Create our Space

        >>> browser.getControl('Create').click()
        >>> 'Welcome to your new Space' in browser.contents
        True
        >>> print browser.url
        http://nohost/plone/new-id

    Check that template was created with correct properties.

        >>> 'new-id' in portal
        True
        >>> space = portal['new-id']
        >>> print space.portal_type
        collective.spaces.space
        >>> print space.id
        new-id
        >>> print space.title
        Custom title
        >>> space.Creator() == testing.TEST_USER_NAME
        True


    Our current user should have local roles in this context.

        >>> [x for x in space.get_local_roles() if x[0] == \\
        ...     testing.TEST_USER_NAME][0]
        ('test-user', ('Contributor', 'Editor', 'Reader', 'Reviewer', 'Owner'))

    Super.  Let's carry on and login as an adminstrator with the
    Site Administrator role.

        >>> testing.setRoles(portal,testing.TEST_USER_ID,
        ...                  ['Site Administrator'])
        >>> transaction.commit()
        >>> browser.open(portal_url)
        >>> 'Site Setup' in browser.contents
        True

    Try and create another Space.

        >>> browser.open(portal_url+'/@@create-space')

    Enter details onto the form to create the Space. Let's try creating
    a Space with a pre-existing ID.

        >>> browser.getControl('Space ID').value = 'new-id'
        >>> browser.getControl('Space Title').value = \\
        ...     'Custom title'
        >>> browser.getControl('Create').click()

    Check the errors are reported.

        >>> 'There were some errors' in browser.contents
        True
        >>> 'This ID is reserved' in browser.contents
        True

    Fix this up.

        >>> browser.getControl('Space ID').value = 'example-item-cloned'

    We've intentionally selected an ID of a template that we know
    doesn't exist to check the validator. This implicitly tests the
    presence of the Template ID field since we're an admin.

        >>> 'non-existant' not in portal
        True
        >>> browser.getControl('Template ID').value = 'non-existant'
        >>> browser.getControl('Create').click()

    Check the errors that happened. The ID field should be correct now
    and the Template ID should be problematic.

        >>> 'This ID is reserved' in browser.contents
        False
        >>> 'An object of this ID does not exist' in browser.contents
        True

    Correct the template ID. We'll use something that doesn't even have
    to be a Space content instance to prove we can successfully.

        >>> browser.getControl('Template ID').value = 'example-item'

    Create our clone of this item

        >>> browser.getControl('Create').click()

    Test this new copy exists and that everything worked.

        >>> print browser.url
        http://nohost/plone/example-item-cloned
        >>> clone = portal['example-item-cloned']
        >>> print clone.portal_type
        News Item
        >>> print clone.title
        Custom title

    Test the Cancel button for the form.

        >>> browser.open(portal_url+'/@@create-space')
        >>> browser.getControl('Cancel').click()
        >>> browser.url == portal_url
        True

    Test that the error message is displayed if something goes wrong
    when cloning the Space.

        >>> browser.open(portal_url+'/@@create-space')

    Swap out the _clone function for something that will *definitely*
    throw an exception.

        >>> from collective.spaces import utils
        >>> utils._clone_old = utils._clone
        >>> utils._clone = lambda: 1/0

        >>> browser.getControl('Space ID').value = 'this-will-break'
        >>> browser.getControl('Space Title').value = 'Test Breakage'
        >>> browser.getControl('Create').click()

        >>> "An error occurred whilst creating your Space" in browser.contents
        True

        >>> utils._clone = utils._clone_old

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
        """Handle the process of creating the user's new Space at site root.

        This function utilises the manage_clone functionality associated
        with Plone in order to reproduce a given template. Administrative
        users are presented with the option to change the template ID whereas
        normal users cannot do so to prevent security issues.
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        space_id = str(data['id'])
        space_title = str(data['space_title'])
        template_id = 'space-template'

        #Only load the template_id from the request if allowed
        if checkPermission('collective.spaces.AddSpace', self.context):
            template_id = str(data.get('template_id', u'space-template'))

        membership_tool = getToolByName(self.context, 'portal_membership')
        member = membership_tool.getAuthenticatedMember()
        member_id = member.getUserName()

        try:
            template = self.context[template_id]
            new_space = utils._clone(self.context, template, space_id)
            new_space.setTitle(space_title)
            new_space.setCreators(member_id)
            new_space.manage_setLocalRoles(member_id, ALL_ROLES)
            new_space.reindexObject()

            #If okay, then redirect to the new Space
            IStatusMessage(self.request).addStatusMessage(
                _(u"Welcome to your new Space! Start adding content"
                  u"and sharing with others."),
                "info"
            )

            space_url = new_space.absolute_url()
            self.request.response.redirect(space_url)
        except:
            self.status = _(u"An error occurred whilst creating your Space \
                            with this ID. Please try again or contact your \
                            site administrator if issues persist.")

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
)
grok.global_adapter(TemplateIdValidator)
