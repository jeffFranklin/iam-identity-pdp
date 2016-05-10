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
    profile = Profile()
    profile.netid = netid
    person = get_person(netid)

    # grab the next uwhr or hepps url if there is one
    hr_url = next((url for key, url in person.identifiers.items()
                   if key in ('uwhr', 'hepps')),
                  None)  # default to None
    if hr_url:
        # set source, eid to the last two items following slashes.
        (source, eid) = hr_url.split('/')[-2:]
        employee = get_employee(eid, source=source)
        profile.employee = EmployeeProfile(dct=dict(
            phone_numbers=employee.wp_phone,
            titles=employee.wp_title,
            departments=employee.wp_department))

    if 'sdb' in person.identifiers:
        # Get and set the SDB student data (need to inquire by netid first
        # to find studentid or system key)--and only get this if such an
        # identifier exists for that person
        # split identifier URI into components
        system_key = person.identifiers['sdb'].split('/')[-1]
        student = get_student(system_key)
        profile.student = StudentProfile(dct=dict(
            clazz=student.wp_title[0],  # only ever one value
            phone_numbers=student.wp_phone,
            majors=student.wp_department
        ))

    name = get_name(netid)
    profile.preferred = PreferredNameParts(dct=dict(
        full=name.display_cname,
        first=name.display_fname,
        middle=name.display_mname,
        last=name.display_lname))
    profile.official_name = name.formal_cname
    profile.preferred_name = name.display_cname
    return profile


def get_person(netid):  # TODO fix this to use student id
    """
    Look up IRWS student data by netid (for mock...system key in real life).
    """
    try:
        # TODO fix this to use student id
        irws_person = IRWS().get_person(netid=netid)
        if not irws_person:
            raise ServiceError('could not find person')
    except Exception as e:
        raise ServiceError(e)
    return irws_person


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


# uwhr is default--we can override to use HEPPS for now
def get_employee(eid, source='uwhr'):
    """
    Look up IRWS employee data by eid
    defaults to uwhr--override to hepps until HRP finishes
    """
    try:
        # person = IRWS().get_person() # don't need?
        uwhr_person = IRWS().get_uwhr_person(eid=eid, source=source)
        if not uwhr_person:
            raise ServiceError('no ' + source + ' entry')
    except Exception as e:
        raise ServiceError(e)
    return uwhr_person


def get_student(system_key):  # TODO fix this to use student id
    """
    Look up IRWS student data by netid (for mock...system key in real life).
    """
    try:
        # Strictly speaking, iam-restools seems to want a studentid (sid)
        # but system_key is the "official" IRWS validid for a student.
        # IRWS will look up a student in the SDB source with either one,
        # meaning the URLS are the same, so I am feeding the method
        # a system key (mattjm 2016-05-06)
        sdb_person = IRWS().get_sdb_person(sid=system_key)
        if not sdb_person:
            raise ServiceError('no SDB entry')
    except Exception as e:
        raise ServiceError(e)
    return sdb_person
