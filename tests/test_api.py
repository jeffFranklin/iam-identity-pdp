from pdp.api import Name, Publish, Profile
from pdp.mock import mock_irws_person
import logging
import json
from pytest import fixture, raises
from idbase.exceptions import NotFoundError, BadRequestError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_name_get_with_display_name(rf):
    request = rf.get('/api/name', netid='joe')
    response = Name().GET(request)
    assert response.status_code == 200
    request.user.set_full_name.assert_called_once_with('James Average Student')
    name = json.loads(response.content)
    formals = {'formal_lname': 'BLO', 'formal_fname': 'JO'}
    assert (formals == {k: v for k, v in name.items() if k in formals})
    displays = {'display_lname': 'Student',
                'display_mname': 'Average', 'display_fname': 'James'}
    assert (displays == {k: v for k, v in name.items() if k in displays})


def test_name_get_no_display_name(rf):
    request = rf.get('/api/name', netid='javerage')
    response = Name().GET(request)
    assert response.status_code == 200
    request.user.set_full_name.assert_called_once_with('JO BLO')
    displays = {'display_lname': '', 'display_mname': '', 'display_fname': ''}
    name = json.loads(response.content)
    assert (displays == {k: v for k, v in name.items() if k in displays})


def test_name_put(rf):
    name = json.dumps({
        'first': 'Jane', 'middle': 'X', 'last': 'Doe'})
    request = rf.put('/api/name', netid='joe', data=name)
    response = Name().PUT(request)
    assert response.status_code == 200
    request.user.set_full_name.assert_called_once_with('Jane X Doe')


def test_name_put_bad_json(rf):
    name = json.dumps({'foo': 'bar'})
    with raises(BadRequestError):
        Name().PUT(rf.put('/', data=name))


def test_name_put_bad_name(rf):
    name = json.dumps(dict(first='', middle='', last='blow'))
    with raises(BadRequestError):
        Name().PUT(rf.put('/', data=name))


def test_publish_get(caches, source, publish_value, rf):
    kwargs = {'identifiers': [source],
              source + '_update': dict(wp_publish=publish_value)}
    mock_person('joe', caches, **kwargs)
    states = {'Y': 'yes', 'N': 'no', 'E': 'no email', 'X': 'X'}
    request = rf.get('/api/publish', netid='joe')
    response = Publish().GET(request)
    assert response.status_code == 200
    assert json.loads(response.content) == {'publish': states[publish_value]}


def test_publish_get_not_found(rf):
    with raises(NotFoundError):
        Publish().GET(rf.get('/', netid='noworker'))


def test_publish_put(rf, put_option, caches, source):
    mock_person('joe', caches, identifiers=[source])
    stored_states = {'yes': 'Y', 'no': 'N', 'no email': 'E'}
    response = Publish().PUT(rf.put('/', netid='joe',
                                    data=json.dumps({'publish': put_option})))
    assert response.status_code == 200
    joe_hr = json.loads(
        caches[1]['/registry-dev/v1/person/{}/joe'.format(source)])
    assert joe_hr['person'][0]['wp_publish'] == stored_states[put_option]


def test_publish_put_no_worker(rf):
    with raises(NotFoundError):
        Publish().PUT(
            rf.put('/', netid='noworker', data=json.dumps({'publish': 'yes'})))


def test_publish_bad_option(rf):
    with raises(BadRequestError):
        Publish().PUT(
            rf.put('/', netid='joe', data=json.dumps({'publish': 'X'})))


def test_profile(rf):
    response = Profile().GET(rf.get('/', netid='joe'))
    assert response['netid'] == 'joe'


@fixture(params=('yes', 'no', 'no email'))
def put_option(request):
    return request.param


@fixture(params=['hepps', 'uwhr'])
def source(request):
    return request.param


@fixture(params=['Y', 'N', 'E', 'X'])
def publish_value(request):
    return request.param


@fixture(autouse=True)
def caches(irws_file_cache, restclients_file_cache):
    caches = [irws_file_cache, restclients_file_cache]
    mock_person('joe', caches, formal=dict(first='JO', last='BLO'),
                display=dict(first='James', middle='Average', last='Student'))
    mock_person('javerage', caches, formal=dict(first='JO', last='BLO'),
                display=dict(first='', middle='', last=''))
    mock_person('noworker', caches, identifiers={})
    return caches


def mock_person(netid, caches, **kwargs):
    resources = mock_irws_person(netid, **kwargs)
    [cache.update(resources) for cache in caches]
