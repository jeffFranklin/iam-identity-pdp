from django.test import LiveServerTestCase
import urllib3
import simplejson as json
import pytest

class NameTests(LiveServerTestCase):

    def test_name_get(self):
        name = self._get_name()
        assert ({'display_lname', 'display_fname', 'display_mname'}
                <= set(name.keys()))

    def test_name_put_basic(self):
        self._put_success(('Dwight', 'David', 'Adams'))

    def test_name_put_good_characters(self):
        self._put_success(('!$&\' *-,.?^_`{}~', '', 'Adams'))

    def test_name_put_no_first_name(self):
        self._put_fail(('', 'David', 'Adams'))

    def test_name_put_no_first_name(self):
        self._put_fail(('Dwight', 'David', ''))

    def test_name_put_name_too_long(self):
        # 80 magic number
        bad_names = [
            ('f' * 30, 'm' * 30, 'l' * 19),
            ('f' * 40, '', 'l' * 40)
            ]
        for bad_name in bad_names:
            # one less should do it
            self._put_success((bad_name[0],
                               bad_name[1],
                               bad_name[2][:-1]))
            self._put_fail(bad_name)

    def test_name_put_name_part_too_long(self):
        # 65 individual name part magic number
        bad_names = [
            ('f' * 65, 'm', 'l'),
            ('f', 'm' * 65, 'l'),
            ('f', 'm', 'l' * 65),
            ]
        for bad_name in bad_names:
            # one less should do it
            good_name = tuple([i[:-1] if len(i) == 65 else i for i in bad_name])
            self._put_success(good_name)
            self._put_failure(bad_name)

    def test_name_put_bad_characters(self):
        bad_chars = '"():;<>[\]|@%+#'
        for bad_char in bad_chars:
            self._put_fail(('f' + bad_char + 'f', 'm', 'l'))

    def test_name_put_no_utf8(self):
        self._put_fail((u'Jos\xe9', 'Average', 'User'))

    def _put_success(self, name):
        response = self._put_name_response(name)
        assert response.status == 200
        get_name = self._get_name()
        assert name[0] == get_name['display_fname']
        assert name[1] == get_name['display_mname']
        assert name[2] == get_name['display_lname']

    def _put_fail(self, name):
        response = self._put_name_response(name)
        assert response.status == 400

    def _put_name_response(self, name):
        put_name = {'display_fname': name[0],
                    'display_mname': name[1],
                    'display_lname': name[2]}

        return self.http.request('PUT',
                                 '{}/id/api/name'.format(self.live_server_url),
                                 headers={'Content-Type': 'application/json'},
                                 body=json.dumps(put_name))
        
    def _get_name(self):
        r = self.http.request('GET', '{}/id/api/name'.format(self.live_server_url))
        assert r.status == 200
        return json.loads(r.data)
        

    @property
    def http(self):
        if not getattr(self, '_http', None):
            self._http = urllib3.PoolManager()
        return self._http
