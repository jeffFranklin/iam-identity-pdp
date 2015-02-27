from restclients.dao import MY_DAO
from restclients.exceptions import DataFailureException
from restclients.mock_http import MockHTTP


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

        return response

    def put_preferred_name_by_netid(self, netid, body):
        dao = IRWS_DAO()
        url = '/irws/{netid}'.format(netid=netid)
        response = dao.putURL(url,
                              {'Accept': 'application/json'},
                              '')

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return response


class IrwsString(object):
    def __init__(self):
        self.data = ('{"firstName": "Joe",'
                     ' "middleName": "Bob",'
                     ' "lastName": "McDoog"}')

    def getURL(self, url, headers):
        response = MockHTTP()
        response.status = 200
        # arbitrary json for now
        response.data = self.data
        return response

    def putURL(self, url, headers, body):
        response = MockHTTP()
        responses.status = 200
        response.data = body
        return response
