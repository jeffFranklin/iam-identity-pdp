from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from userservice.user import UserService
import logging
from authz_group import Group
from django.contrib.auth.decorators import login_required

@login_required
def support(request):
    #timer = Timer()
    logger = logging.getLogger(__name__)

    user_service = UserService()
    user_service.get_user()
    override_error_username = None
    override_error_msg = None
    # Do the group auth here.

    if not hasattr(settings, "USERSERVICE_ADMIN_GROUP"):
        print "You must have a group defined as your admin group."
        print 'Configure that using USERSERVICE_ADMIN_GROUP="foo_group"'
        raise Exception("Missing USERSERVICE_ADMIN_GROUP in settings")

    actual_user = user_service.get_original_user()
    if not actual_user:
        raise Exception("No user in session")

    g = Group()
    group_name = settings.USERSERVICE_ADMIN_GROUP
    is_admin = g.is_member_of_group(actual_user, group_name)
    if is_admin == False:
        return render_to_response('no_access.html', {})

    if "override_as" in request.POST:
        new_user = request.POST["override_as"].strip()
        validation_module = _get_validation_module()
        validation_error = validation_module(new_user)
        if validation_error is None:
            logger.info("%s is impersonating %s",
                        user_service.get_original_user(),
                        new_user)
            user_service.set_override_user(new_user)
        else:
            override_error_username = new_user
            override_error_msg = validation_error

    if "clear_override" in request.POST:
        logger.info("%s is ending impersonation of %s",
                    user_service.get_original_user(),
                    user_service.get_override_user())
        user_service.clear_override()

    context = {
        'original_user': user_service.get_original_user(),
        'override_user': user_service.get_override_user(),
        'override_error_username': override_error_username,
        'override_error_msg': override_error_msg,
    }

    try:
        template.loader.get_template("userservice/user_override_extra_info.html")
        context['has_extra_template'] = True
        context['extra_template'] = 'userservice/user_override_extra_info.html'
    except template.TemplateDoesNotExist:
        # This is a fine exception - there doesn't need to be an extra info
        # template
        pass

    try:
        template.loader.get_template("userservice/user_override_wrapper.html")
        context['wrapper_template'] = 'userservice/user_override_wrapper.html'
    except template.TemplateDoesNotExist:
        context['wrapper_template'] = 'support_wrapper.html'
        # This is a fine exception - there doesn't need to be an extra info
        # template
        pass


    return render_to_response('support.html',
                              context,
                              context_instance=RequestContext(request))

def _get_validation_module():
    if hasattr(settings, "USERSERVICE_VALIDATION_MODULE"):
        module, attr = getattr(settings, "USERSERVICE_VALIDATION_MODULE").rsplit('.', 1)
        try:
            mod = import_module(module)
        except ImportError, e:
            raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                       (module, e))
        try:
            validation_module = getattr(mod, attr)
        except AttributeError:
            raise ImproperlyConfigured('Module "%s" does not define a '
                               '"%s" class' % (module, attr))
        return validation_module
    else:
        return validate
    
    
def validate(username):
    error_msg = "No override user supplied"
    if (len(username) > 0):
        error_msg = None
    return error_msg
