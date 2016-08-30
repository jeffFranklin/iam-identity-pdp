from pdp.views import index
from mock import patch
from django.shortcuts import render
import logging

logging.basicConfig(level=logging.DEBUG)


@patch('pdp.views.render', side_effect=render)
def test_index(mock_render, rf):
    request = rf.get('/', netid='foo')
    response = index(request)
    assert response.status_code == 200
    mock_render.assert_called_once_with(request, 'cascade.html')


def test_index_no_login(rf):
    request = rf.get('/', netid=None)
    request.uwnetid = None
    response = index(request)
    assert response.status_code == 302
    assert response.url == '/profile/login/'
