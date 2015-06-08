from pdp.views.api.name import Name
import logging
import json
from restclients.exceptions import InvalidIRWSName, DataFailureException
from pdp.test.util import TestWithMocks, mock_request

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestName(TestWithMocks):

    def setup_class(self):
        self.mock_items = {'irws': 'pdp.views.api.name.IRWS'}

    def test_name_get(self):
        name = Name()
        request = mock_request()
        get_name = self.irws.return_value.get_name_by_netid
        get_name.return_value.json_data.return_value = {'foo': 'bar'}

        response = name.GET(request)

        get_name.assert_called_once_with('jjj')
        assert response.status_code == 200
        response_name = json.loads(response.content)
        assert response_name['foo'] == 'bar'

    def test_name_put(self):
        name = Name()
        request = mock_request({'foo': 'bar'})

        self.irws.return_value.put_name_by_netid.return_value = {
            'baz': 'bar'}

        response = name.PUT(request)

        self.irws.return_value.put_name_by_netid.assert_called_once_with(
            'jjj', request.body)
        assert response.status_code == 200
        assert json.loads(response.content)['baz'] == 'bar'

    def test_name_put_bad_name(self):
        name = Name()
        request = mock_request({})
        put_name = self.irws.return_value.put_name_by_netid
        put_name.side_effect = InvalidIRWSName('bad name')

        response = name.PUT(request)
        assert response.status_code == 400

    def test_name_put_data_exception(self):
        dfe = DataFailureException('j', 300, '')
        self.irws.return_value.put_name_by_netid.side_effect = dfe
        exception_caught = False
        try:
            Name().PUT(mock_request({}))
        except:
            exception_caught = True
        assert exception_caught
