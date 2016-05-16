from pdp.api import Name, Publish, Profile
from pdp.mock import mock_irws_person
import logging
import json
from pytest import fixture, raises, mark
from idbase.exceptions import NotFoundError, BadRequestError
from idbase.exceptions import InvalidSessionError

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


@mark.parametrize('put_option', ('Y', 'N', 'E'))
@mark.parametrize('source', ('hepps', 'uwhr'))
def test_publish_put(rf, caches, put_option, source):
    netid = 'joe'
    resources = mock_person(
        netid, caches, identifiers=[source])
    joe_hr_key = next(key for key in resources
                      if source in key and '/v2/' in key)
    req = rf.put('joe?value={}'.format(put_option), netid='joe')
    response = Publish().PUT(req, netid='joe')
    assert response == {'publish': put_option}
    joe_hr = json.loads(caches[0][joe_hr_key])
    assert joe_hr['person'][0]['wp_publish'] == put_option


def test_publish_put_no_worker(rf):
    with raises(NotFoundError):
        req = rf.put('noworker?value=Y', netid='noworker')
        Publish().PUT(req, netid='noworker')


def test_publish_bad_option(rf):
    with raises(BadRequestError):
        req = rf.put('joe?value=X', netid='joe')
        Publish().PUT(req, netid='joe')


def test_publish_netid_switch(rf):
    with raises(InvalidSessionError):
        req = rf.put('joe?value=X', netid='joe')
        Publish().PUT(req, netid='jack')


def test_profile(rf):
    response = Profile().GET(rf.get('/', netid='joe'))
    assert response['netid'] == 'joe'


@fixture(autouse=True)
def caches(irws_file_cache):
    caches = [irws_file_cache]
    mock_person('joe', caches, formal=dict(first='JO', last='BLO'),
                display=dict(first='James', middle='Average', last='Student'))
    mock_person('javerage', caches, formal=dict(first='JO', last='BLO'),
                display=dict(first='', middle='', last=''))
    mock_person('noworker', caches, identifiers={})
    return caches


def mock_person(netid, caches, **kwargs):
    resources = mock_irws_person(netid, **kwargs)
    [cache.update(resources) for cache in caches]
    return resources
