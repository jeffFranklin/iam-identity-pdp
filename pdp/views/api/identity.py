# identity apis

import logging
from django.http import HttpResponse
import json
import re

from restclients.irws import IRWS

from pdp.views.rest_dispatch import RESTDispatch, data_not_found


# get/set publish flag

class Publish(RESTDispatch):

    def GET(self, request):

        logger = logging.getLogger('pdp')
        logger.info("identity/publish api")
        remote_user = re.sub(r'@.*', '', request.user.username)
        irws = IRWS()
        ident = irwsClient.get_identity_by_netid(remote_user)
        wp_publish = 'true'
        if 'hepps' in ident.identifiers:
            uri = ident.identifiers['hepps']
            hepps = irwsClient.get_hepps_person_by_uri(uri)
            if hepps.wp_publish != 'Y':
                wp_publish = 'false'
        resp = {}
        resp['wp_publish'] = wp_publish
        return HttpResponse(json.dumps(resp),
                            content_type='application/json')

    def PUT(self, request):

        logger = logging.getLogger('pdp')
        logger.debug('identity/publish api put')
        remote_user = re.sub(r'@.*', '', request.user.username)

        irws = IRWS()

        # pn = irws.put_publish_by_netid(remote_user, request.body)
        errtxt = '{"message":
                   "Saving publish preference is not yet implemented."}'
        return HttpResponse(json.dumps(errtxt),
                            content_type='application/json',
                            status=501)
