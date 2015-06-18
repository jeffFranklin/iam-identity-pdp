# identity apis

import logging
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseBadRequest
import json
from restclients.exceptions import DataFailureException, IRWSPersonNotFound
from restclients.irws import IRWS
from pdp.views.rest_dispatch import RESTDispatch
from pdp.util import Util

logger = logging.getLogger(__name__)

# get/set publish flag


class Publish(RESTDispatch):

    publish_options = {'N': 'no', 'Y': 'yes', 'E': 'no email'}
    publish_options_reverse = {value: key
                               for key, value in publish_options.items()}

    def GET(self, request):
        logger.debug("publish api get for user {}".format(
            request.user.username))
        netid = Util.netid_from_remote_user(request.user.username)
        try:
            person = IRWS().get_hepps_person_by_netid(netid)
            response = HttpResponse(
                self._person_object_to_json(person),
                content_type='application/json')
        except IRWSPersonNotFound:
            response = HttpResponseNotFound()
        except DataFailureException as dfe:
            logger.info(str(dfe))
            raise dfe
        return response

    def PUT(self, request):
        logger.info('publish api put for user {}'.format(
            request.user.username))
        netid = Util.netid_from_remote_user(request.user.username)

        irws = IRWS()
        try:
            # success or exception
            irws.post_hepps_person_by_netid(
                netid,
                self._json_to_irws_json(request.body))
            response = HttpResponse(json.dumps({'message': 'successful put'}),
                                    content_type='application_json',
                                    status=200)
        except DataFailureException as dfe:
            logger.info(str(dfe))
            raise dfe
        except IRWSPersonNotFound:
            logger.info('attempted to post for non-hepps person ' + netid)
            response = HttpResponseNotFound()
        except Exception as e:
            logger.info('exception {} occurred: {}'.format(
                type(e).__name__, str(e)))
            response = HttpResponseBadRequest()

        return response

    def _person_object_to_json(self, person):
        if person.wp_publish in Publish.publish_options:
            publish_flag = Publish.publish_options[person.wp_publish]
        else:
            # unexpected value, just return it
            publish_flag = person.wp_publish
        return json.dumps(
            {'publish': publish_flag})

    def _json_to_irws_json(self, data):
        try:
            person = json.loads(data)
            irws_json = json.dumps(
                {'wp_publish': Publish.publish_options_reverse[
                    person['publish']]})
        except:
            raise ValueError('bad json from browser')
        return irws_json
