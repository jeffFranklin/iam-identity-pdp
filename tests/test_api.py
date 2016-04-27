from pdp.api import Name, Publish, Profile
import logging
import json
import re
from pytest import fixture, raises
from idbase.exceptions import NotFoundError, BadRequestError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_name_get(rf):
    request = rf.get('/api/name', netid='joe')
    response = Name().GET(request)
    assert response.status_code == 200
    request.user.set_full_name.assert_called_once_with('JO BLO')
    name = json.loads(response.content)
    formals = {'formal_lname': 'BLO', 'formal_fname': 'JO'}
    assert (formals == {k: v for k, v in name.items() if k in formals})
    displays = {'display_lname': '', 'display_mname': '', 'display_fname': ''}
    assert (displays == {k: v for k, v in name.items() if k in displays})


def test_name_get_with_display_name(rf):
    request = rf.get('/api/name', netid='javerage')
    response = Name().GET(request)
    assert response.status_code == 200
    request.user.set_full_name.assert_called_once_with('James Average Student')
    displays = {'display_lname': 'Student', 'display_mname': 'Average',
                'display_fname': 'James'}
    name = json.loads(response.content)
    assert (displays == {k: v for k, v in name.items() if k in displays})


def test_name_put(rf):
    name = json.dumps({
        'display_fname': 'Jane', 'display_mname': 'X', 'display_lname': 'Doe'})
    request = rf.put('/api/name', netid='joe', data=name)
    response = Name().PUT(request)
    assert response.status_code == 200
    request.user.set_full_name.assert_called_once_with('Jane X Doe')


@fixture(autouse=True)
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
    update_file_cache(irws_file_cache)
    return irws_file_cache


def test_publish_get(irws_file_cache, source, publish_value, rf):
    update_file_cache(irws_file_cache, source=source,
                      publish_value=publish_value)
    states = {'Y': 'yes', 'N': 'no', 'E': 'no email', 'X': 'X'}
    request = rf.get('/api/publish', netid='joe')
    response = Publish().GET(request)
    assert response.status_code == 200
    assert json.loads(response.content) == {'publish': states[publish_value]}


def test_publish_get_not_found(rf, file_cache):
    with raises(NotFoundError):
        Publish().GET(rf.get('/', netid='noworker'))


def test_publish_put(rf, put_option, irws_file_cache, source):
    update_file_cache(irws_file_cache, source=source)
    stored_states = {'yes': 'Y', 'no': 'N', 'no email': 'E'}
    response = Publish().PUT(rf.put('/', netid='joe',
                                    data=json.dumps({'publish': put_option})))
    assert response.status_code == 200
    joe_hr = json.loads(irws_file_cache[irws_file_cache['joe_hr_key']])
    assert joe_hr['person'][0]['wp_publish'] == stored_states[put_option]


def test_publish_put_no_worker(rf, file_cache):
    with raises(NotFoundError):
        Publish().PUT(
            rf.put('/', netid='noworker', data=json.dumps({'publish': 'yes'})))


def test_publish_bad_option(rf, file_cache):
    with raises(BadRequestError):
        Publish().PUT(
            rf.put('/', netid='joe', data=json.dumps({'publish': 'X'})))


@fixture(params=('yes', 'no', 'no email'))
def put_option(request):
    return request.param


@fixture(params=['hepps', 'uwhr'])
def source(request):
    return request.param


@fixture(params=['Y', 'N', 'E', 'X'])
def publish_value(request):
    return request.param


def update_file_cache(file_cache, source='uwhr', publish_value='N'):
    joe_hr_key = '/registry-dev/v1/person/{source}/123'.format(
        source=source)
    file_cache.update({
        '/registry-dev/v1/person?uwnetid=joe': json.dumps({
            "person": [{"identity": {
                "regid": "00deadbeef", "lname": "STUDENT",
                "fname": "JAMES AVERAGE",
                "identifiers": {
                    "hepps": re.sub(r'/registry-dev/v1', '', joe_hr_key)}}}],
            "totalcount": 1}),
        joe_hr_key: json.dumps({
                "person": [{
                    "validid": "123456775", "regid": "00deadbeef",
                    "lname": "STUDENT", "fname": "JIMMY",
                    "wp_publish": publish_value, "category_code": "XXX",
                    "category_name": "bah"}],
                "totalcount": 1}),
        '/registry-dev/v1/person?uwnetid=noworker': json.dumps({
            "person": [{"identity": {
                "regid": "00deadbeef", "lname": "NOTAWORKER",
                "fname": "JAMES AVERAGE",
                "identifiers": {}}}],
            "totalcount": 1}),
    })
    file_cache.update(dict(joe_hr_key=joe_hr_key))
    return file_cache


def test_profile(rf):
    response = Profile().GET(rf.get('/', netid='joe'))
    assert response['netid'] == 'joe'
