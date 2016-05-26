from pdp.api import Name, Publish, Profile, verify_netid
from pdp.mock import mock_irws_person
import logging
import json
from pytest import fixture, raises, mark
from idbase.exceptions import NotFoundError, BadRequestError
from idbase.exceptions import InvalidSessionError
from mock import MagicMock


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_name_get_with_display_name(rf):
    request = rf.get('/api/name', netid='joe')
    name = Name().GET(request, netid='joe')
    assert name == {'first': 'James', 'middle': 'Average', 'last': 'Student',
                    'full': 'James Average Student'}


def test_name_get_no_display_name(rf):
    request = rf.get('/api/name', netid='javerage')
    name = Name().GET(request, netid='javerage')
    assert name == {'first': '', 'middle': '', 'last': '', 'full': ''}


def test_name_get_wrong_netid(rf):
    request = rf.get('/api/name', netid='javerage')
    with raises(InvalidSessionError):
        Name().GET(request, netid='joe')


def test_name_put(rf):
    name = json.dumps({
        'first': 'Jane', 'middle': 'X', 'last': 'Doe'})
    request = rf.put('/api/name', netid='joe', data=name)
    name = Name().PUT(request, netid='joe')
    assert name == {'first': 'Jane', 'middle': 'X', 'last': 'Doe',
                    'full': 'Jane X Doe'}


def test_name_put_wrong_netid(rf):
    with raises(InvalidSessionError):
        name = json.dumps({'first': 'Jane', 'middle': 'X', 'last': 'Doe'})
        request = rf.get('/api/name/', netid='javerage')
        Name().PUT(request, netid='joe')


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


@mark.parametrize('netid', ['joe', None, ''])
def test_verify_netid_same_netid(rf, netid):
    assert verify_netid(rf.get('/', netid='joe'), netid=netid) == 'joe'


def test_verify_netid_not_authorized(gws, rf):
    gws.is_profile_admin.return_value = False
    with raises(InvalidSessionError):
        verify_netid(rf.get('/', netid='joe'), netid='notjoe')


def test_verify_netid_is_admin(gws, rf):
    """
    Check that joe can impersonate bob and bob can't impersonate joe.
    """
    gws.is_profile_admin = lambda *x, **y: y['netid'] == 'joe'
    req = rf.get('/', netid='joe')
    assert verify_netid(req, netid='bob') == 'bob'
    with raises(InvalidSessionError):
        verify_netid(rf.get('/', netid='bob'), netid='joe')


@fixture
def gws(monkeypatch):
    client = MagicMock()
    monkeypatch.setattr('pdp.api.GWS', lambda: client)
    return client


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
