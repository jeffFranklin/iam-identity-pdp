import re
import os
import logging
import time

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render_to_response


from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template import Context, loader

from django.conf import settings
from userservice.user import UserService
from pdp.views.rest_dispatch import invalid_session
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
import simplejson as json
from restclients.pws import PWS


logger = logging.getLogger('pdp')


# ------------- login --------------------
#
# login handler:  get userid and some info from shib
#
# ----------------------------------------
def login(request):
    return_url = request.REQUEST.get('postlogin', '/')

    if request.user.is_authenticated():
        logger.info('User = ' + request.user.username)
        remote_user = request.user.username
        logger.info('User = ' + remote_user)

        print(request.META['AJP_displayName'])
        # request.user.first_name='Jim'
        # request.user.last_name='Fox'
        # request.user.save()
        # temporary skip the rest
        logger.info('User %s logged in' % (remote_user))
        return redirect(return_url)

        # use shib names
        if len(request.user.last_name) == 0:
            if 'sn' in request.META:
                request.user.last_name = request.META['sn']
            else:
                request.user.last_name = request.user.username
            if 'givenName' in request.META:
                request.user.first_name = request.META['givenName']
            else:
                request.user.first_name = 'Joe'
            logger.info('New User name={} {}'.format(
                    request.user.first_name,
                    request.user.last_name))

        # allowed aliases are member-of u_netid_<sharedid>_admins
        aliases = []
        if 'isMemberOf' in request.META:
            grpstr = request.META['isMemberOf']
            grps = grpstr.split(';')
            for g in grps:
                if re.search(
                        '^urn:mace:washington.edu:groups:u_netid_.*_admins$',
                        g) != None:
                    a = re.sub(
                        r'urn:mace:washington.edu:groups:u_netid_(.*)_admins',
                        r'\1',
                        g)
                    aliases.append(a)
        logger.info('%(request.user.username)s logged in')
    else:
        # import pdb; pdb.set_trace()
        # probably testing without authn in place
        # create fake 'nobody'
        user = auth.authenticate(remote_user='nobody')
        logger.error("Unauthenticated user")
        request.user = user
        print 'at javerage: ' 
        print request.user.is_authenticated()
        auth.login(request, user)
        request.user.save()
    return redirect(return_url)


def logout(request):
    logger.info('logout user: ' + request.user.username)
    auth.logout(request)
    return redirect('/Shibboleth.sso/Logout')


@login_required(redirect_field_name='postlogin')
def index(request, template=None):
    # remove the @washington.edu
    remote_user = re.sub(r'@.*', '', request.user.username)
    logger.info('remote user=' + remote_user)

    userid = UserService().get_user()
    logger.info('userservice user=' + userid)

    # get some info about this user from PWS
    pwsClient = PWS()
    pws = pwsClient.get_person_by_netid(remote_user)

    context = {
       'remote_user': remote_user,
       'pws_info': pws,
    }

    return render(request, 'page.html', context)
