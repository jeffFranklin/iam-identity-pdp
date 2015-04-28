import logging
from django.http import HttpResponse, HttpResponseBadRequest
import json
import re

from restclients.irws import IRWS
from restclients.exceptions import DataFailureException

from pdp.views.rest_dispatch import RESTDispatch, data_not_found


class Name(RESTDispatch):

    def GET(self, request):

        logger = logging.getLogger('pdp')
        logger.info("name api")
        remote_user = re.sub(r'@.*', '', request.user.username)
        irws = IRWS()
        name = irws.get_name_by_netid(remote_user)
        return HttpResponse(json.dumps(name.json_data()),
                            content_type='application/json')

    def PUT(self, request):

        logger = logging.getLogger('pdp')
        logger.debug('name api put')
        remote_user = re.sub(r'@.*', '', request.user.username)

        try:
            pn = IRWS().put_name_by_netid(remote_user, request.body)
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
