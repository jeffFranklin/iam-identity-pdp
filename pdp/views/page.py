import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie


logger = logging.getLogger('pdp')


@login_required
@ensure_csrf_cookie
def index(request, template=None):
    show_publish = (False if (request.GET.get('show_publish', 'off').lower()
                              in ('0', 'off', 'false'))
                    else True)

    return render(request, 'page.html', {'show_publish': show_publish})


@login_required
@ensure_csrf_cookie
def cascade(request):
    return render(request, 'cascade.html')
