from restclients.dao import MY_DAO
from restclients.exceptions import DataFailureException
from restclients.mock_http import MockHTTP
from collections import namedtuple
import simplejson as json
import logging

logger = logging.getLogger(__name__)

PrefNameModel = namedtuple(
    'PrefNameModel',
    ['firstName', 'middleName', 'lastName',])

class IRWS_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('irws', url, headers)

    def putURL(self, url, headers, body):
        return self._putURL('irws', url, headers, body)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_IRWS_DAO_CLASS', IrwsString)


class IRWS(object):


    def get_preferred_name_by_netid(self, netid):
        dao = IRWS_DAO()
        url = '/irws/{netid}'.format(netid=netid)
        response = dao.getURL(url, {'Accept': 'application/json'})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._pref_name_from_json(response.data)

    def put_preferred_name_by_netid(self, netid, json_string):
        # right now they're the same but eventually our api
        # model and what goes into irws could be different
        pn = self._pref_name_from_json(json_string)
        dao = IRWS_DAO()
        url = '/irws/{netid}'.format(netid=netid)
        response = dao.putURL(url,
                              {'Accept': 'application/json'},
                              json.dumps(pn))

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        # return value should probably be something else
        return pn

    def _pref_name_from_json(self, data):
        """
        Read the data into our namedtuple to validate our json
        """
        logger.debug('_pref_name_from_json for ' + data)
        json_object = json.loads(data)
        try:
            pn = PrefNameModel(**json_object)
        except:
            raise Exception("invalid preferred name")
        return pn


class IrwsStringData:
    data = ('{"firstName": "Joe",'
            ' "middleName": "Bob",'
            ' "lastName": "McDoog"}')


class IrwsString(object):
    def getURL(self, url, headers):
        response = MockHTTP()
        response.status = 200
        # arbitrary json for now
        response.data = IrwsStringData.data
        return response

    def putURL(self, url, headers, body):
        response = MockHTTP()
        response.status = 200
        # persist it in memory
        IrwsStringData.data = body
        response.data = body
        return response
