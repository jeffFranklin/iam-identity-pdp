from authz_group.authz_implementation.all_ok import AllOK
from authz_group.authz_implementation.all_fail import AllFail
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

class Group():
    def __init__(self):
        self._backend = self._get_backend_module()

    def group_membership_url(self, group):
        if hasattr(self._backend, "group_membership_url"):
            return self._backend.group_membership_url(group)
        return None

    def is_member_of_group(self, user_name, group):
        return self._backend.is_member_of_group(user_name, group)

    def group_display_name(self, group_source_id):
        if hasattr(self._backend, "group_display_name"):
            return self._backend.group_display_name(group_source_id)
        return group_source_id

    def _get_backend_module(self):
        if hasattr(settings, "AUTHZ_GROUP_BACKEND"):
            # This is all taken from django's static file finder
            module, attr = getattr(settings, "AUTHZ_GROUP_BACKEND").rsplit('.', 1)
            try:
                mod = import_module(module)
            except ImportError as e:
                raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                           (module, e))
            try:
                authz_module = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a '
                                   '"%s" class' % (module, attr))
            return authz_module()
        else:
            if settings.DEBUG:
                print("You should set an AUTHZ_GROUP_BACKEND in you settings.py")
                return AllOK()
            else:
                print("You need to set an AUTHZ_GROUP_BACKEND in you settings.py")
                return AllFail()


