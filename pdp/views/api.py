import logging
import json
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from pdp.views.rest_dispatch import RESTDispatch
from pdp.dao import IRWS

logger = logging.getLogger(__name__)


class PrefNameView(View):

    # @login_required
    def get(self, request, *args, **kwargs):
        logger.info("so it's come to this")
        irws = IRWS()
        response = irws.get_preferred_name_by_netid('javerage')
        return HttpResponse(response.data,
                            content_type='application/json')
        # return HttpResponse(json.dumps(context),
        #                     content_type='application/json')

    # @login_required
    def put(self, request, body, *args, **kwargs):
        logger.debug('posting some stuff')
        irws = IRWS()
        response = irws.put_preferred_name_by_netid('javerage', '')
        return HttpResponse(response.data,
                            content_type='application/json')


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
