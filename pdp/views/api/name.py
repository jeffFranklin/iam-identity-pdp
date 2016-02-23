import logging
from django.http import HttpResponse, HttpResponseBadRequest
import json

from restclients.irws import IRWS
from restclients.exceptions import DataFailureException
from pdp.util import full_name_from_object

from idbase.api import RESTDispatch

logger = logging.getLogger(__name__)


class Name(RESTDispatch):

    def GET(self, request):
        logger.debug("name api get for user {}".format(request.user.username))
        irws = IRWS()
        name = irws.get_name_by_netid(request.user.netid)
        request.user.set_full_name(full_name_from_object(name))
        return HttpResponse(json.dumps(name.json_data()),
                            content_type='application/json')

    def PUT(self, request):
        logger.info('name api put for user {}'.format(
            request.user.username))
        try:
            IRWS().put_name_by_netid(request.user.netid, request.body)
            return self.GET(request)
        except DataFailureException as dfe:
            logger.info(str(dfe))
            raise dfe
        except Exception as e:
            logger.info('exception {} occurred: {}'.format(
                type(e).__name__, str(e)))
            response = HttpResponseBadRequest()
        return response
