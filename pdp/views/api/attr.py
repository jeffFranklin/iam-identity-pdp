import logging
import time
from django.shortcuts import render
from django.http import HttpResponse
import simplejson as json
from pdp.views.rest_dispatch import RESTDispatch, data_not_found


class Attr(RESTDispatch):
    """
    Performs actions on resource at /api/attr/.
    """

    def GET(self, request):

        logger = logging.getLogger(__name__)

        logger.info('Attr')
        context = {
            'user': 'spud',
            }
        return render(request, 'attr.html', context)
