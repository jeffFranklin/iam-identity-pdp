from pdp.models import (Profile, PreferredNameParts,
                        StudentProfile, EmployeeProfile, PDSProfile)
from django.conf import settings
from resttools.irws import IRWS as RestToolsIRWS
from idbase.exceptions import ServiceError
try:  # http://asq.googlecode.com/hg-history/1.0/asq/_portability.py
    # Python 2
    from itertools import izip_longest
except ImportError:
    # Python 3
    from itertools import zip_longest as izip_longest


class IRWS(RestToolsIRWS):
    def __init__(self):
        super(self.__class__, self).__init__(settings.IRWS_CLIENT)


def get_profile(netid):
    """Return the profile for a given netid."""
    profile = Profile()
    profile.netid = netid
    person = get_person(netid)

    profile.employee = get_employee(person.identifiers)
    profile.student = get_student(person.identifiers)
    # cast to set() to get unique emails
    profile.emails = list(set(
        (profile.employee.emails if profile.employee else []) +
        (profile.student.emails if profile.student else [])))
    name = get_name(netid)
    profile.preferred = PreferredNameParts(
        full=name.display_cname,
        first=name.display_fname,
        middle=name.display_mname,
        last=name.display_lname)
    profile.official_name = name.formal_cname
    profile.preferred_name = name.display_cname
    profile.pds = get_pdsentry(netid=netid)
    return profile


def get_person(netid):  # TODO fix this to use student id
    """
    Look up IRWS student data by netid (for mock...system key in real life).
    """
    irws_person = IRWS().get_person(netid=netid)
    if not irws_person:
        raise ServiceError('could not find person')
    return irws_person


def get_name(netid):
    """
    Look up an irws name by netid. All people should have a name. Raise a
    ServiceError for all no-names.
    """
    name = IRWS().get_name_by_netid(netid)
    if not name:
        raise ServiceError('no name resource')
    return name


def get_employee(identifiers):
    """
    Look up IRWS employee data given a dictionary of irws identifiers.
    Return an EmployeeProfile, or None if not an active employee.
    """

    # grab the next uwhr or hepps url if there is one
    hr_url = next((url for key, url in identifiers.items()
                   if key in ('uwhr', 'hepps')),
                  None)  # default to None
    if not hr_url:
        return None

    (source, eid) = hr_url.split('/')[-2:]
    employee = IRWS().get_uwhr_person(eid=eid, source=source)
    # set source, eid to the last two items following slashes.

    if employee.status_code != '1':
        return None

    return EmployeeProfile(
        official_name=' '.join(x for x in [employee.fname, employee.lname]
                               if x),
        phone_numbers=employee.wp_phone,
        titles=employee.wp_title,
        departments=employee.wp_department,
        addresses=employee.wp_address,
        emails=employee.wp_email,
        box=employee.mailstop,
        publish=employee.wp_publish,
        titledepts=[', '.join(pair) for pair in izip_longest(
                employee.wp_title,
                employee.wp_department,
                fillvalue='-')]
        )


def get_student(identifiers):
    """
    Look up IRWS student data given a dictionary of irws identifiers.
    Return a StudentProfile, or None if not an active student.
    """
    if 'sdb' not in identifiers:
        return None
    system_key = identifiers['sdb'].split('/')[-1]
    student = IRWS().get_sdb_person(sid=system_key)
    if student.status_code != '1':
        return None
    return StudentProfile(
        official_name=' '.join(x for x in [student.fname, student.lname] if x),
        emails=student.wp_email,
        phone_numbers=student.wp_phone,
        class_majors=[', '.join(pair) for pair in izip_longest(
            student.wp_title, student.wp_department, fillvalue='-')],
        publish=(False if student.wp_publish == 'N' else True)
    )

def get_pdsentry(netid):
    pdsentry = IRWS().get_pdsentry_by_netid(netid=netid)
    # make sure this is a natural person
    if 'uwPerson' in pdsentry.objectclass:
        return PDSProfile(
            pdspreferredname=pdsentry.preferredname
        )
    else:
        raise ServiceError('not a natural person (e.g. shared account)')
