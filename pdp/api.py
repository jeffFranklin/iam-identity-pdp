import logging
from django.http import HttpResponse
import json
from pdp.dao import IRWS
from resttools.exceptions import InvalidIRWSName
from pdp.util import full_name_from_object
from pdp.dao import get_profile
from idbase.api import RESTDispatch
from idbase.exceptions import NotFoundError, BadRequestError
from idbase.exceptions import InvalidSessionError

logger = logging.getLogger(__name__)


class Profile(RESTDispatch):

    def GET(self, request):
        logger.debug(
            'getting profile for {}'.format(request.user.get_username()))
        return get_profile(request.user.netid).to_dict()


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
            data = json.loads(request.body)
            name_args = {key: data[key]
                         for key in ('first', 'middle', 'last')}
        except:
            raise BadRequestError('invalid json')

        try:
            IRWS().put_name_by_netid(request.user.netid, **name_args)
        except InvalidIRWSName as e:
            logger.info(e)
            raise BadRequestError('invalid name')
        return self.GET(request)


class Publish(RESTDispatch):

    def PUT(self, request, netid=None):
        """
        Set the publish value for the given netid according to the query
        parameter in 'value'. Return the new publish flag.
        """
        if netid != request.user.netid:
            raise InvalidSessionError()
        publish_value = request.GET.get('value', '')
        if publish_value not in ('Y', 'N', 'E'):
            raise BadRequestError()
        logger.info('publish api put for user {}'.format(
            request.user.username))

        try:
            person = IRWS().put_hr_person_by_netid(
                request.user.netid,
                wp_publish=publish_value)
        except NotFoundError as nfe:
            logger.info('failed attempt to post for non-employee {}'.format(
                request.user.username))
            raise NotFoundError(nfe)

        return {'publish': person.wp_publish}
