import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from pdp.util import netid_from_remote_user
from restclients.irws import IRWS
from idbase.context_processors import set_logged_in_person


logger = logging.getLogger('pdp')


# ------------- login --------------------
#
# login handler:  get userid and some info from shib
#
# ----------------------------------------
def login(request):
    return_url = request.REQUEST.get('postlogin', '/')
    print 'login: return = ' + return_url

    if request.user.is_authenticated():
        logger.info('User %s logged in' % (request.user.username))
        try:
            name = IRWS().get_name_by_netid(netid_from_remote_user(request.user.username))
            set_logged_in_person()

        except Exception as e:
            logger.exception(e)
        return redirect(return_url)
    else:
        raise Exception('this should never happen')


@login_required(redirect_field_name='postlogin')
def index(request, template=None):
    show_publish = False if request.GET.get('show_publish', 'off').lower() in ('0', 'off', 'false') else True

    return render(request, 'page.html', {'app': settings.APP_CONTEXTS['default'], 'show_publish': show_publish})
