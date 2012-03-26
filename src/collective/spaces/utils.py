from zope.security import checkPermission

from AccessControl.SecurityManagement import getSecurityManager, \
        setSecurityManager, newSecurityManager
from AccessControl.User import UnrestrictedUser

from Products.CMFCore.utils import getToolByName


def elevated_access(fn):
    """ Decorator to grant elevated access temporarily.
    """
    def wrapper(*args, **kwargs):
        context = args[0]
        if checkPermission('collective.spaces.AddSpace', context):
            result = fn(*args, **kwargs)
        else:
            old_sm = getSecurityManager()
            tmp_user = UnrestrictedUser(old_sm.getUser().getId(),
                                        '', ['Contributor'], '')
            tmp_user = tmp_user.__of__(getToolByName(context, 'acl_users'))
            try:
                newSecurityManager(None, tmp_user)
                result = fn(*args, **kwargs)
            except:
                raise
            finally:
                setSecurityManager(old_sm)

        return result

    return wrapper


@elevated_access
def _clone(context, obj, clone_id):
    """ Clone a given object against some context using elevated access.
    """
    return context.manage_clone(obj, clone_id)
