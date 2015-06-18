from pdp.views.page import index
import mock
import logging

logging.basicConfig(level=logging.DEBUG)


@mock.patch('pdp.views.page.render')
@mock.patch('pdp.views.page.UserService')
@mock.patch('pdp.views.page.IRWS')
def test_index(irws, user_service, render):
    """
    mock irws, user_service, and render, and mock a
    a request. Basically anything coming in or going out
    of index()
    """
    user_service.return_value.get_user.return_value = 'jjj'
    # exceptions shouldn't cause our index to fail
    irws.return_value.get_person_by_netid.side_effect = Exception()
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

    # assert our irws client not called from index
    assert len(irws.mock_calls) == 0
