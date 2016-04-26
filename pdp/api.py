import logging
from django.http import HttpResponse
import json
from restclients.irws import IRWS
from restclients.exceptions import InvalidIRWSName, IRWSPersonNotFound
from pdp.util import full_name_from_object
from idbase.api import RESTDispatch
from idbase.exceptions import NotFoundError, BadRequestError

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
        except InvalidIRWSName as e:
            logger.info(e)
            raise BadRequestError('invalid name')
        return self.GET(request)


class Publish(RESTDispatch):

    publish_options = {'N': 'no', 'Y': 'yes', 'E': 'no email'}
    publish_options_reverse = {value: key
                               for key, value in publish_options.items()}

    def GET(self, request):
        logger.debug("publish api get for user {}".format(
            request.user.username))
        netid = request.user.netid
        try:
            person = IRWS().get_hr_person_by_netid(netid)
            response = HttpResponse(
                self._person_object_to_json(person),
                content_type='application/json')
        except IRWSPersonNotFound as nfe:
            logger.debug('failed publish get for non-employee {}'.format(
                request.user.username))
            raise NotFoundError(nfe)
        return response

    def PUT(self, request):
        logger.info('publish api put for user {}'.format(
            request.user.username))

        irws = IRWS()
        try:
            # success or exception
            irws.post_hr_person_by_netid(
                request.user.netid,
                self._json_to_irws_json(request.body))
            response = HttpResponse(json.dumps({'message': 'successful put'}),
                                    content_type='application_json',
                                    status=200)
        except IRWSPersonNotFound as nfe:
            logger.info('failed attempt to post for non-employee {}'.format(
                request.user.username))
            raise NotFoundError(nfe)

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
            raise BadRequestError('bad json from browser')
        return irws_json
