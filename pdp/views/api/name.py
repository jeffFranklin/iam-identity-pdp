import logging
from django.http import HttpResponse, HttpResponseBadRequest
import json

from restclients.irws import IRWS
from restclients.exceptions import DataFailureException

from pdp.views.rest_dispatch import RESTDispatch
from pdp.util import netid_from_remote_user

logger = logging.getLogger(__name__)


class Name(RESTDispatch):

    def GET(self, request):
        logger.debug("name api get for user {}".format(request.user.username))
        netid = netid_from_remote_user(request.user.username)
        irws = IRWS()
        name = irws.get_name_by_netid(netid)
        return HttpResponse(json.dumps(name.json_data()),
                            content_type='application/json')

    def PUT(self, request):
        logger.info('name api put for user {}'.format(
            request.user.username))
        netid = netid_from_remote_user(request.user.username)

        try:
            pn = IRWS().put_name_by_netid(netid, request.body)
            response = HttpResponse(json.dumps(pn),
                                    content_type='application/json')
        except DataFailureException as dfe:
            logger.info(str(dfe))
            raise dfe
        except Exception as e:
            logger.info('exception {} occurred: {}'.format(
                type(e).__name__, str(e)))
            response = HttpResponseBadRequest()
        return response
