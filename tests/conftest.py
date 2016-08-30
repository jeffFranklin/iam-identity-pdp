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
        request.uwnetid = netid
        request.session = {}


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
