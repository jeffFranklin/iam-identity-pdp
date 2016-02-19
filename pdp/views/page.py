import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings


logger = logging.getLogger('pdp')


@login_required(redirect_field_name='postlogin')
def index(request, template=None):
    show_publish = False if request.GET.get('show_publish', 'off').lower() in ('0', 'off', 'false') else True

    return render(request, 'page.html', {'app': settings.APP_CONTEXTS['default'], 'show_publish': show_publish})
