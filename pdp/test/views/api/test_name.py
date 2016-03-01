from pdp.views.api.name import Name
import logging
import json
from mock import MagicMock
from pytest import fixture

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_name_get(rf, file_cache):
    request = rf.get('/api/name', netid='joe')
    response = Name().GET(request)
    assert response.status_code == 200
    request.user.set_full_name.assert_called_once_with('JO BLO')
    name = json.loads(response.content)
    formals = {'formal_lname': 'BLO', 'formal_fname': 'JO'}
    assert (formals == {k: v for k, v in name.items() if k in formals})
    displays = {'display_lname': '', 'display_mname': '', 'display_fname': ''}
    assert (displays == {k: v for k, v in name.items() if k in displays})


def test_name_get_with_display_name(rf, file_cache):
    request = rf.get('/api/name', netid='javerage')
    response = Name().GET(request)
    assert response.status_code == 200
    request.user.set_full_name.assert_called_once_with('James Average Student')
    displays = {'display_lname': 'Student', 'display_mname': 'Average',
                'display_fname': 'James'}
    name = json.loads(response.content)
    assert (displays == {k: v for k, v in name.items() if k in displays})


def test_name_put(rf, file_cache):
    name = json.dumps({
        'display_fname': 'Jane', 'display_mname': 'X', 'display_lname': 'Doe'})
    request = rf.put('/api/name', netid='joe', data=name)
    response = Name().PUT(request)
    assert response.status_code == 200
    request.user.set_full_name.assert_called_once_with('Jane X Doe')


@fixture
def file_cache(irws_file_cache):
    irws_file_cache.update({
        '/registry-dev/v1/name/uwnetid=joe': json.dumps({
            'name': [{
                'validid': '123',
                'formal_fname': 'JO', 'formal_sname': 'BLO'}
            ]
        }),
        '/registry-dev/v1/name/uwnetid=javerage': json.dumps({
            'name': [{
                'validid': '123',
                'formal_fname': 'JO', 'formal_sname': 'BLO',
                'display_fname': 'James', 'display_mname': 'Average',
                'display_sname': 'Student'}
            ]}),
    })
    return irws_file_cache
