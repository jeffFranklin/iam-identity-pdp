from pdp.models import (Profile, PreferredNameParts,
                        StudentProfile, EmployeeProfile)
from django.conf import settings
from resttools.irws import IRWS as RestToolsIRWS
from idbase.exceptions import ServiceError


class IRWS(RestToolsIRWS):
    def __init__(self):
        super(self.__class__, self).__init__(settings.IRWS_CLIENT)


def get_profile(netid):
    """Return the profile for a given netid."""
    # TODO: This goes away after we plug in all the right attributes
    fake_profile = dict(
        netid=netid,
        emails=['tjohn1234@uw.edu'],
        student=dict(
            phone_numbers=['(425)333-4444'],
            clazz='Frosh',
            major='Sociology'
        ),
        employee=dict(
            phone_numbers=['(206)123-2222'],
            official_name='TIMOTHY ROBERT JOHNSON',
            emails=['tjohn1234@uw.edu'],
            address='107 NE 45th St. #505 Seattle WA 98105'
        )
    )
    # TODO: We eventually won't pass in fake_profile
    profile = Profile(dct=fake_profile)
    name = get_name(netid)
    profile.preferred = PreferredNameParts(dct=dict(
        full=name.display_cname,
        first=name.display_fname,
        middle=name.display_mname,
        last=name.display_lname))

    # Get and set the SDB student data (need to inquire by netid first
    # to find studentid or system key)--and only get this if such an
    # identifier exists for that person
    student = get_student(netid)
    profile.student = StudentProfile(dct=dict(
        clazz=student.wp_title,
        phone_numbers=student.wp_phone,
        major=student.department


    ))

    profile.official_name = name.formal_cname
    profile.preferred_name = name.display_cname
    return profile


def get_name(netid):
    """
    Look up an irws name by netid. All people should have a name. Raise a
    ServiceError for all errors and no-names.
    """
    try:
        name = IRWS().get_name_by_netid(netid)
        if not name:
            raise ServiceError('no name resource')
    except Exception as e:
        raise ServiceError(e)
    return name


def get_student(netid):  # TODO fix this to use student id
    """
    Look up IRWS student data by netid (for mock...system key in real life).
    """
    try:
        # TODO fix this to use student id
        sdb_person = IRWS().get_sdb_person(sid=netid)
        if not sdb_person:
            raise ServiceError('no SDB entry')
    except Exception as e:
        raise ServiceError(e)
    return sdb_person


def get_student(netid):  # TODO fix this to use student id
    """
    Look up IRWS student data by netid (for mock...system key in real life).
    """
    try:
        # TODO fix this to use student id
        sdb_person = IRWS().get_sdb_person(sid=netid)
        if not sdb_person:
            raise ServiceError('no SDB entry')
    except Exception as e:
        raise ServiceError(e)
    return sdb_person
