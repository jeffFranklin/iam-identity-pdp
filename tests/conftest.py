from pytest import fixture
from mock import MagicMock


class WrappedRequestFactory(object):
    def __init__(self, rf):
        self.rf = rf

    def get(self, path, data=None, secure=False, netid=None, **extra):
        request = self.rf.get(path, data=data, secure=secure, **extra)
        self._add_attributes(request, netid=netid)
        return request

    def put(self, path, data=None, secure=False, netid=None, **extra):
        request = self.rf.put(path, data=data, secure=secure, **extra)
        self._add_attributes(request, netid=netid)
        return request

    def _add_attributes(self, request, netid=None):
        request.user = self._get_user(netid)
        request.resolver_match = MagicMock()

    def _get_user(self, netid=None):
        user = MagicMock()
        if netid is None:
            user.is_authenticated.return_value = False
        else:
            user.is_authenticated.return_value = True
            user.netid = netid
            user.username = netid + '@washington.edu'
        return user


@fixture
def rf(rf):
    return WrappedRequestFactory(rf)


@fixture
def irws_file_cache():
    from resttools.dao_implementation.irws import File
    orig_cache = File._cache_db
    File._cache_db = {}

    def fin():
        File._cache_db = orig_cache
    return File._cache_db
