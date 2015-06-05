import re
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from userservice.user import UserService
from django.contrib import auth
from restclients.irws import IRWS
from pdp.util import Util


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
        logger.info('User = ' + request.user.username)
        remote_user = request.user.username
        logger.info('User = ' + remote_user)

        if 'AJP_displayName' in request.META:
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
        print('at javerage: ')
        print(request.user.is_authenticated())
        auth.login(request, user)
        request.user.save()
    return redirect(return_url)


def logout(request):
    logger.info('logout user: ' + request.user.username)
    auth.logout(request)
    return redirect('/Shibboleth.sso/Logout')


@login_required(redirect_field_name='postlogin')
def index(request, template=None):
    remote_user = Util.netid_from_remote_user(request.user.username)
    logger.info('remote user=' + remote_user)

    show_publish = False
    if (request.GET.get('show_publish', 'off').lower()
            not in ('0', 'off', 'false')):
        show_publish = True

    userid = UserService().get_user()
    logger.info('userservice user=' + userid)

    # get some info about this user from IRWS
    irwsClient = IRWS()
    name = irwsClient.get_name_by_netid(remote_user)

    context = {
       'remote_user': remote_user,
       'irws_name': name,
       'show_publish': show_publish,
    }

    return render(request, 'page.html', context)
