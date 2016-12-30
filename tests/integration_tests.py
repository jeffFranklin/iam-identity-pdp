"""
Tests to make sure our APIs and Live backend APIs (IRWS) are working together
correctly.  These are run by ansible/install.yml at the time we deploy
to develop. Failure here will block a deploy to develop.
"""
import simplejson as json
from pytest import fixture
import requests
import re


@fixture(scope='session')
def client(live_server):

    class Session(requests.Session):
        def get(self, url, **kwargs):
            response = super(self.__class__, self).get(
                live_server + url, **kwargs)
            if 'csrftoken' in self.cookies:
                self.headers.update(
                    {'X-CSRFToken': self.cookies.get('csrftoken')})
            return response

        def put(self, url, **kwargs):
            return super(self.__class__, self).put(live_server + url, **kwargs)

    client = Session()
    return client


@fixture
def client_idtest55(client, settings):
    settings.USE_MOCK_LOGIN = True
    settings.MOCK_LOGIN_USER = 'idtest55@washington.edu'
    settings.SESSION_COOKIE_SECURE = False  # to get the CSRF cookie
    client.get(settings.LOGIN_URL)
    return client


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


def test_get_basic(client_idtest55):
    response = client_idtest55.get('/profile/api/name')
    assert response.status_code == 200


@fixture(params=good_names, ids=good_name_ids)
def good_name(request):
    return request.param


def test_put_success(client_idtest55, good_name):
    name = dict(first=good_name[0], middle=good_name[1],
                last=good_name[2])
    response = client_idtest55.put('/profile/api/name/idtest55',
                                   data=json.dumps(name))
    assert response.status_code == 200
    response = client_idtest55.get('/profile/api/name/idtest55')
    name_response = json.loads(response.content)
    assert good_name[0] == name_response['first']
    assert good_name[1] == name_response['middle']
    assert good_name[2] == name_response['last']

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


def test_put_invalid(client_idtest55, bad_name):
    name = dict(first=bad_name[0], middle=bad_name[1],
                last=bad_name[2])
    response = client_idtest55.put('/profile/api/name',
                                   data=json.dumps(name))
    assert response.status_code == 400
