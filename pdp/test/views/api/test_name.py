from pdp.views.api.name import Name
import mock
import logging
import json
from restclients.exceptions import InvalidIRWSName, DataFailureException

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestName(object):

    def setup_method(self, method):
        logger.debug('setting up method {}'.format(method.__name__))
        self.patchers = {'irws': mock.patch('pdp.views.api.name.IRWS')}

        for attr, patcher in self.patchers.iteritems():
            setattr(self, attr, patcher.start())

    def teardown_method(self, method):
        for patcher in self.patchers.values():
            patcher.stop()

    def test_name_get(self):
        name = Name()
        request = self._mock_request()
        get_name = self.irws.return_value.get_name_by_netid
        get_name.return_value.json_data.return_value = {
            'foo': 'bar'}

        response = name.GET(request)

        get_name.assert_called_once_with('jjj')
        assert response.status_code == 200
        response_name = json.loads(response.content)
        assert response_name['foo'] == 'bar'

    def test_name_put(self):
        name = Name()
        request = self._mock_request({'foo': 'bar'})

        self.irws.return_value.put_name_by_netid.return_value = {
            'baz': 'bar'}

        response = name.PUT(request)

        self.irws.return_value.put_name_by_netid.assert_called_once_with(
            'jjj', request.body)
        assert response.status_code == 200
        assert json.loads(response.content)['baz'] == 'bar'

    def test_name_put_bad_name(self):
        name = Name()
        request = self._mock_request({})
        put_name = self.irws.return_value.put_name_by_netid
        put_name.side_effect = InvalidIRWSName('bad name')

        response = name.PUT(request)
        assert response.status_code == 400

    def test_name_put_data_exception(self):
        dfe = DataFailureException('j', 300, '')
        self.irws.return_value.put_name_by_netid.side_effect = dfe
        exception_caught = False
        try:
            Name().PUT(self._mock_request({}))
        except:
            exception_caught = True
        assert exception_caught

    def _mock_request(self, body=None):
        request = mock.MagicMock()
        request.user.username = 'jjj@washington.edu'
        if body is not None:
            request.body = json.dumps(body)
        return request
