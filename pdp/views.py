import logging

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie


logger = logging.getLogger('pdp')


@login_required
@ensure_csrf_cookie
def index(request, template=None):
    return render(request, 'page.html')


@login_required
@ensure_csrf_cookie
def cascade(request):
    return render(request, 'cascade.html')
