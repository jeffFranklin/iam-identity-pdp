import logging
from django.http import HttpResponse
import json
from pdp.dao import IRWS, GWS
from resttools.exceptions import InvalidIRWSName, ResourceNotFound
from pdp.util import full_name_from_object
from pdp.dao import get_profile
from idbase.api import RESTDispatch
from idbase.exceptions import NotFoundError, BadRequestError
from idbase.exceptions import InvalidSessionError

logger = logging.getLogger(__name__)


class Profile(RESTDispatch):

    def GET(self, request, netid=None):
        verified_netid = verify_netid(request, netid=netid)
        logger.debug(
            'getting profile for {}'.format(verified_netid))
        return get_profile(verified_netid).to_dict()


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
        verified_netid = verify_netid(request, netid=netid)
        publish_value = request.GET.get('value', '')
        if publish_value not in ('Y', 'N', 'E'):
            raise BadRequestError()
        logger.info('publish api put for user {}'.format(
            verified_netid))

        try:
            person = IRWS().post_hr_person_by_netid(
                verified_netid,
                wp_publish=publish_value)
        except ResourceNotFound as nfe:
            logger.info('failed attempt to post for non-employee {}'.format(
                verified_netid))
            raise NotFoundError(nfe)

        return {'publish': person.wp_publish}


def verify_netid(request, netid=None):
    """
    Check that the netid coming in from an API request is that of the logged in
    user or that the logged in user has the authority to impersonate
    the netid. Return the netid if so, otherwise raise InvalidSessionError.
    """
    verified_netid = None
    if not netid or netid == request.user.netid:
        verified_netid = request.user.netid
    elif GWS().is_profile_admin(netid=request.user.netid):
        logger.info('IMPERSONATION of netid {} by {}'.format(
            netid, request.user.netid))
        verified_netid = netid
    if not verified_netid:
        logger.error('FAILED IMPERSONATION of netid {} by {}'.format(
            netid, request.user.netid))
        raise InvalidSessionError()
    return verified_netid
