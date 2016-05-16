from pdp.dao import get_profile
from pytest import fixture, raises
from idbase.exceptions import ServiceError
from mock import MagicMock
from pdp.mock import mock_irws_person

irws_root = '/registry-dev/v2'


def test_get_profile(irws):
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


def test_profile_employee_student(irws_cache):
    irws_cache.update(mock_irws_person('empstu', irws_root=irws_root))
    profile = get_profile('empstu')
    assert profile.student
    assert profile.employee


def test_profile_employee_only(irws_cache):
    irws_cache.update(mock_irws_person('employee', irws_root=irws_root,
                                       identifiers=['hepps']))
    profile = get_profile('employee')
    assert profile.employee
    assert not profile.student


def test_profile_student_only(irws_cache):
    irws_cache.update(mock_irws_person('student', irws_root=irws_root,
                                       identifiers=['sdb']))
    profile = get_profile('student')
    assert profile.student
    assert not profile.employee


@fixture
def irws(monkeypatch):
    """
    Mock irws client. Use this if you want to mock behaviors of the
    client itself.
    """
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


def test_profile_unset_defaults(irws_cache):
    irws_cache.update(mock_irws_person(
        'empstu', irws_root=irws_root, clazz=[],
        majors=[], student_phone_number=[],
        employee_address=[], employee_depts=[], employee_titles=[],
        employee_phone_number=[]
    ))
    profile = get_profile('empstu')
    assert profile.student.clazz == ''
    assert profile.student.emails == []
    assert profile.student.majors == []
    assert profile.student.phone_numbers == []
    assert profile.employee.emails == []
    assert profile.employee.phone_numbers == []
    assert profile.employee.titledepts == []
    assert profile.employee.titles == []
    assert profile.employee.departments == []


def test_profile_publish_flag(irws_cache):
    irws_cache.update(mock_irws_person(
        'empstu', irws_root=irws_root,
        employee_publish='E', student_publish='N'))
    profile = get_profile('empstu')
    assert profile.employee.publish == 'E'
    assert not profile.student.publish


@fixture
def irws_cache(request):
    """
    Mock irws cache. Use this if you want to mock a person by modifying
    the file-based mock dao.
    """
    from resttools.dao_implementation.irws import File
    old_cache = File._cache_db
    File._cache_db = {}

    def fin():
        File._cache_db = old_cache
    request.addfinalizer(fin)
    return File._cache_db
