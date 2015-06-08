import logging
import mock
import simplejson as json

logger = logging.getLogger(__name__)


class TestWithMocks(object):
    """
    A class that inherits this defines an dictionary mock_items whose
    keys are the attribute names to hold our mocks, and whose values
    are the classes to be mocked
    """

    def setup_method(self, method):
        logger.debug('setting up method {}'.format(method.__name__))
        self._patchers = []
        if hasattr(self, 'mock_items'):
            for attr, item in self.mock_items.items():
                patcher = mock.patch(item)
                setattr(self, attr, patcher.start())
                self._patchers.append(patcher)

    def teardown_method(self, method):
        for patcher in self._patchers:
            patcher.stop()


def mock_request(body=None):
        request = mock.MagicMock()
        request.user.username = 'jjj@washington.edu'
        if body is not None:
            request.body = json.dumps(body)
        return request
