from pdp.models import (Profile, PreferredNameParts,
                        StudentProfile, EmployeeProfile)
from django.conf import settings
from resttools.irws import IRWS as RestToolsIRWS
from resttools.exceptions import DataFailureException
from resttools.dao import IRWS_DAO
from idbase.exceptions import ServiceError, NotFoundError, BadRequestError
import json
try:  # http://asq.googlecode.com/hg-history/1.0/asq/_portability.py
    # Python 2
    from itertools import izip_longest
except ImportError:
    # Python 3
    from itertools import zip_longest as izip_longest


class IRWS(RestToolsIRWS):
    def __init__(self):
        super(self.__class__, self).__init__(settings.IRWS_CLIENT)

    def get_hr_person_by_netid(self, netid):
        # TODO: This likely can come out after Publish() refactor.
        hr_url = self._get_hr_url(netid)
        if hr_url:
            source, eid = hr_url.split('/')[-2:]
            hr_person = self.get_uwhr_person(eid, source=source)
        else:
            raise NotFoundError('not hr person: {}'.format(netid))
        return hr_person

    def put_hr_person_by_netid(self, netid, wp_publish=None):
        # TODO: move into resttools once we've finalized the design.
        if wp_publish not in ('Y', 'N', 'E'):
            raise BadRequestError('Invalid publish option')

        hr_url = self._get_hr_url(netid)
        if hr_url:
            url = '/{}/v2{}'.format(self._service_name, hr_url)
            hr_data = {'person': [{'wp_publish': wp_publish}]}
            response = IRWS_DAO(self._conf).putURL(
                url, {"Accept": "application/json"}, json.dumps(hr_data))
            if response.status != 200:
                raise DataFailureException(url, response.status, response.data)
        else:
            raise NotFoundError('not hr person: {}'.format(netid))
        source, eid = hr_url.split('/')[-2:]
        return self.get_uwhr_person(eid, source=source)

    def _get_hr_url(self, netid):
        person = self.get_person(netid=netid)
        hr_url = None
        if person:
            hr_url = next((url for key, url in person.identifiers.items()
                           if key in ('uwhr', 'hepps')),
                          None)
        return hr_url


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
            departments=employee.wp_department,
            addresses=employee.wp_address,
            box=employee.mailstop,

            titledepts=[', '.join(pair) for pair in izip_longest(
                    employee.wp_title,
                    employee.wp_department,
                    fillvalue='-')]

            ))

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
