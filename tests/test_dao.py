from pdp.dao import get_profile


def test_get_profile():
    profile = get_profile('jeff')
    assert profile.netid == 'jeff'
