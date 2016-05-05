from pdp.dao import get_profile
from pytest import fixture, raises
from idbase.exceptions import ServiceError
from mock import MagicMock


def test_get_profile():
    profile = get_profile('jeff')
    assert profile.netid == 'jeff'


def test_profile_name(irws):
    profile = get_profile('jeff')
    irws.get_name_by_netid.assert_called_once_with('jeff')
    assert profile.preferred_name == 'J O E'
    assert profile.official_name == 'JOE'
    assert profile.preferred.first == 'J'
    assert profile.preferred.middle == 'O'
    assert profile.preferred.last == 'E'
    assert profile.preferred.full == 'J O E'


def test_profile_name_none(irws):
    irws.get_name_by_netid.return_value = None
    with raises(ServiceError):
        get_profile('jeff')


@fixture(autouse=True)
def irws(monkeypatch):
    client = MagicMock()
    # mock name resource
    name = client.get_name_by_netid.return_value
    name.display_cname = 'J O E'
    name.display_lname = 'E'
    name.display_mname = 'O'
    name.display_fname = 'J'
    name.formal_cname = 'JOE'

    monkeypatch.setattr('pdp.dao.IRWS', lambda: client)
    return client
