from django.test import LiveServerTestCase
import urllib3
import simplejson as json

class NameTests(LiveServerTestCase):

    def test_name_get(self):
        http = urllib3.PoolManager()
        r = http.request('GET', '{}/id/api/name'.format(self.live_server_url))
        assert r.status == 200
        name = json.loads(r.data)
        assert name['formal_lname'] == 'FRANKLIN'

    def test_name_put(self):
        http = urllib3.PoolManager()
        r = http.request('GET', '{}/id/api/name'.format(self.live_server_url))
        assert r.status == 200
        orig_name = json.loads(r.data)
        r = http.request('PUT', '{}/id/api/name'.format(self.live_server_url),
                         headers={'Content-Type':'application/json'},
                         body=json.dumps({'display_lname': 'Franklin',
                                          'display_mname': '',
                                          'display_fname': 'Jeff'}))
        assert r.status == 200
