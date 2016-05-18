from pdp.dao import get_profile, get_employee, get_student
from pytest import fixture, raises
from idbase.exceptions import ServiceError
from mock import MagicMock
from pdp.mock import mock_irws_person, source_person
import json

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
        employee_phone_number=[], employee_emails=[], student_emails=[]
    ))
    profile = get_profile('empstu')
    assert profile.student.emails == []
    assert profile.student.class_majors == []
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


def test_get_employee(irws_cache):
    source = 'hepps'
    employee = source_person(
        source, irws_root=irws_root,
        netid='joe', formal={'first': 'J', 'last': 'B'},
        employee_publish='E', employee_phone_number=['123', '456'],
        employee_emails=['a@b', 'c@d'],
        employee_address=['USA'], mailstop='666',
        employee_titles=['VIP', 'MLA'], employee_depts=['French', 'Art'])
    uri = next(key for key in employee)
    irws_cache.update({uri: json.dumps(employee[uri])})
    employee_profile = get_employee({source: uri})
    assert employee_profile.to_dict() == dict(
        official_name=u'J B', phone_numbers=[u'123', u'456'],
        emails=[u'a@b', u'c@d'], addresses=[u'USA'],
        departments=[u'French', u'Art'], titles=[u'VIP', u'MLA'], box=u'666',
        titledepts=[u'VIP, French', u'MLA, Art'], publish=u'E'
    )


def test_get_employee_not_employee(irws_cache):
    assert not get_employee({'sdb': '/foo/123'})


def test_get_employee_not_active(irws_cache):
    formeremp = mock_irws_person('formeremp', irws_root=irws_root,
                                 identifiers=['hepps'],
                                 hepps_update={'status_code': '3'})
    irws_cache.update(formeremp)
    hepps_uri = next(uri for uri in formeremp if '/person/hepps/' in uri)
    assert not get_employee({'hepps': hepps_uri})


def test_get_student(irws_cache):
    student = mock_irws_person(
        'stu', irws_root=irws_root, identifiers=['sdb'],
        sdb_update=dict(
            fname='J', lname='F', wp_title=['Fresh'], wp_phone=['567', '890'],
            wp_department=['Gen', 'Stu'], wp_publish='N',
            wp_email=['e@f', 'g@h']))
    irws_cache.update(student)
    sdb_uri = next(uri for uri in student if '/person/sdb/' in uri)
    student_profile = get_student({'sdb': sdb_uri})
    assert student_profile.to_dict() == dict(
        official_name=u'J F', phone_numbers=[u'567', u'890'],
        class_majors=[u'Fresh, Gen', u'-, Stu'],
        emails=[u'e@f', u'g@h'], publish=False)


def test_get_student_not_student(irws_cache):
    assert not get_student({'hepps': '/foo/132'})


def test_get_student_not_active(irws_cache):
    fmrstud = mock_irws_person('fmrstud', irws_root=irws_root,
                               identifiers=['sdb'],
                               sdb_update={'status_code': '3'})
    irws_cache.update(fmrstud)
    sdb_uri = next(uri for uri in fmrstud if '/person/sdb/' in uri)
    assert not get_student({'sdb': sdb_uri})


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
