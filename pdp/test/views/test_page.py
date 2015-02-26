from pdp.views.page import index
import mock
import logging

logging.basicConfig(level=logging.DEBUG)


@mock.patch('pdp.views.page.render')
@mock.patch('pdp.views.page.UserService')
@mock.patch('pdp.views.page.PWS')
def test_index(pws, user_service, render):
    """
    mock pws, user_service, and render, and mock a
    a request. Basically anything coming in or going out
    of index()
    """
    user_service.return_value.get_user.return_value = 'jjj'
    pws.return_value.get_person_by_netid.return_value = 'foo'
    request = mock.MagicMock()
    request.user.username = 'javerage@washington.edu'

    """Run the thing we're testing"""
    index(request)

    """
    Do our assertions. Here we check that javerage@washington.edu
    got turned into javerage and that we call pws with that.
    Lastly we check that render was called with the right arguments:
    our mock request, page.html, and the dictionary we built up in
    index()
    """
    logging.debug('pws mock calls: {}'.format(pws.mock_calls))
    pws.return_value.get_person_by_netid.assert_called_once_with('javerage')
    logging.debug('render mock calls: {}'.format(render.mock_calls))
    render.assert_called_once_with(request, 'page.html',
                                   {'remote_user': 'javerage',
                                    'pws_info': 'foo'})
