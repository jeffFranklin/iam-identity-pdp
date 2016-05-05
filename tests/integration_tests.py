from django.test import override_settings
from django.conf import settings
import simplejson as json
from pytest import fixture
import requests
import re


@fixture(scope='session')
def client_idtest55(live_server):
    with override_settings(
            DEBUG=True,
            MOCK_LOGIN_USER='idtest55@washington.edu',
            LOGIN_URL='/id/mocklogin',
            MIDDLEWARE_CLASSES=(
                ['idbase.middleware.MockLoginMiddleware'] +
                settings.MIDDLEWARE_CLASSES),
            LOGGING=None):
        # We need to hard-set DEBUG to True because Django's test runner
        # sets it to False regardless of what's in settings.
        session = requests.session()
        # this will trigger a login to mocklogin and send us a csrftoken.
        session.get(live_server + '/id/')
        session.headers.update(
            {'X-CSRFToken': session.cookies.get('csrftoken')})
    return session

good_names = [
    ('Dwight', 'David', 'Adams'),
    ('!$&\' *-,.?^_`{}~#+%', '', 'Adams'),
    ('D+wight', 'D+avid', 'A+dams'),
    ('D%3C%20wight', 'D%3C%20avid', 'A%3C%20dams'),
    ('f' * 29, 'm' * 30, 'l' * 19),
    ('f' * 39, '', 'l' * 40),
    ('f' * 64, 'm', 'l'),
    ('f', 'm' * 64, 'l'),
    ('f', 'm', 'l' * 64),
    ('D#wight', 'D#avid', 'A#dams'),
]
good_name_ids = [re.sub(r'\.', 'dot', '-'.join(n)) for n in good_names]


def test_get_basic(client_idtest55, live_server):
    response = client_idtest55.get(live_server + '/id/api/name')
    assert response.status_code == 200


@fixture(params=good_names, ids=good_name_ids)
def good_name(request):
    return request.param


def test_put_success(client_idtest55, live_server, good_name):
    name = dict(first=good_name[0], middle=good_name[1],
                last=good_name[2])
    response = client_idtest55.put(
        live_server + '/id/api/name',
        data=json.dumps(name))
    assert response.status_code == 200
    response = client_idtest55.get(live_server + '/id/api/name')
    name_response = json.loads(response.content)
    assert good_name[0] == name_response['display_fname']
    assert good_name[1] == name_response['display_mname']
    assert good_name[2] == name_response['display_lname']

bad_char_names = [('Dw{}ght'.format(c), 'David', 'Adams')
                  for c in '"():;<>[\]|@']
bad_names = [
    ('', 'David', 'Adams'),
    ('Dwight', 'David', ''),
    ('f' * 30, 'm' * 30, 'l' * 19),
    ('f' * 40, '', 'l' * 40),
    ('f' * 65, 'm', 'l'),
    ('f', 'm' * 65, 'l'),
    ('f', 'm', 'l' * 65),
    (u'Jos\xe9', 'Average', 'User')
] + bad_char_names
bad_name_ids = [u'-'.join(n).encode('utf8') for n in bad_names]


@fixture(params=bad_names, ids=bad_name_ids)
def bad_name(request):
    return request.param


def test_put_invalid(client_idtest55, live_server, bad_name):
    name = dict(first=bad_name[0], middle=bad_name[1],
                last=bad_name[2])
    response = client_idtest55.put(
        live_server + '/id/api/name',
        data=json.dumps(name))
    assert response.status_code == 400
