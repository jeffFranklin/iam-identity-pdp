from pdp.views.api.name import Name
import mock
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@mock.patch('pdp.views.api.name.IRWS')
def test_name_get(irws):
    name = Name()
    request = mock.MagicMock()
    request.user.username = 'jjj@washington.edu'
    irws.return_value.get_name_by_netid.return_value.json_data.return_value = {
        'foo': 'bar'}

    response = name.GET(request)

    irws.return_value.get_name_by_netid.assert_called_once_with('jjj')
    assert response.status_code == 200
    response_name = json.loads(response.content)
    assert response_name['foo'] == 'bar'


@mock.patch('pdp.views.api.name.IRWS')
def test_name_put(irws):
    name = Name()
    request = mock.MagicMock()
    request.user.username = 'jjj@washington.edu'
    request.body = json.dumps({'foo': 'bar'})
    irws.return_value.put_name_by_netid.return_value = {
        'baz': 'bar'}

    response = name.PUT(request)

    irws.return_value.put_name_by_netid.assert_called_once_with(
        'jjj', request.body)
    assert response.status_code == 200
    assert json.loads(response.content)['baz'] == 'bar'
