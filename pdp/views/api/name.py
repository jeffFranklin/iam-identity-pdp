import logging
from django.http import HttpResponse
import json
import re

from restclients.irws import IRWS

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

        irws = IRWS()
        pn = irws.put_name_by_netid(remote_user, request.body)
        return HttpResponse(json.dumps(pn),
                            content_type='application/json')
