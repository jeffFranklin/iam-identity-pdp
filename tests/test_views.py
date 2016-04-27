from pdp.views import index, cascade
from mock import patch
from django.shortcuts import render
import logging

logging.basicConfig(level=logging.DEBUG)


@patch('pdp.views.render', side_effect=render)
def test_index(mock_render, rf):
    request = rf.get('/', netid='foo')
    response = index(request)
    assert response.status_code == 200
    mock_render.assert_called_once_with(
        request, 'page.html', {'show_publish': False})


def test_index_no_login(rf):
    request = rf.get('/', netid=None)
    request.user.is_authenticated = lambda: False
    response = index(request)
    assert response.status_code == 302
    assert response.url == '/id/login/?next=/'


@patch('pdp.views.render', side_effect=render)
def test_index_show_publish(mock_render, rf):
    request = rf.get('/?show_publish', netid='foo')
    response = index(request)
    assert response.status_code == 200
    mock_render.assert_called_once_with(
        request, 'page.html', {'show_publish': True})


def test_cascade(rf):
    response = cascade(rf.get('/', netid='joe'))
    assert response.status_code == 200
