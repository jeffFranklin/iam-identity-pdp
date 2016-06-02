from pdp.models import (Profile, PreferredNameParts,
                        StudentProfile, EmployeeProfile)
from pdp.mock import mock_irws_resources, mock_gws_resources
from django.conf import settings
from resttools.irws import IRWS as RestToolsIRWS
from resttools.gws import GWS as RestToolsGWS
from idbase.exceptions import ServiceError
import logging
import re
try:  # http://asq.googlecode.com/hg-history/1.0/asq/_portability.py
    # Python 2
    from itertools import izip_longest
except ImportError:
    # Python 3
    from itertools import zip_longest as izip_longest

logger = logging.getLogger(__name__)


class IRWS(RestToolsIRWS):

    is_mock_set = False

    def __init__(self):
        if (settings.IRWS_CONF.get('RUN_MODE', 'Live') == 'File' and
                not IRWS.is_mock_set):
            logger.info('setting mock data.')
            mock_irws_resources()
            IRWS.is_mock_set = True
        super(self.__class__, self).__init__(settings.IRWS_CONF)


class GWS(RestToolsGWS):

    is_mock_set = False

    def __init__(self):
        if (settings.GWS_CONF.get('RUN_MODE', 'Live') == 'File' and
                not GWS.is_mock_set):
            mock_gws_resources()
            GWS.is_mock_set = True
        super(self.__class__, self).__init__(settings.GWS_CONF)

    def is_profile_admin(self, netid=None):
        """
        Return whether a given netid can impersonate others for troubleshooting
        purposes. Return False unless the netid is a member of group
        pointed at by settings.PROFILE_IMPERSONATORS_GROUP. Absence of the
        setting should always return False.
        """
        admin_group = getattr(settings, 'PROFILE_IMPERSONATORS_GROUP', None)

        return (admin_group and
                netid and
                self.is_effective_member(admin_group, netid))

    def is_publish_hidden(self, netid=None):
        """
        Return whether a given netid can't preview the publish update
        interaction. Controlled by settings.PUBLISH_PREVIEWERS_GROUP, absence
        of the setting deploys the feature to everyone, after which this
        and the pieces that use it should come out.
        """
        preview_group = getattr(settings, 'PUBLISH_PREVIEWERS_GROUP', None)
        return (preview_group and
                netid and
                not self.is_effective_member(preview_group, netid))


def get_profile(netid):
    """Return the profile for a given netid."""
    profile = Profile()
    profile.netid = netid
    person = get_person(netid)

    profile.employee = get_employee(person.identifiers)
    profile.student = get_student(person.identifiers)
    # for email we append @uw.edu to UW NetID
    profile.emails = [netid + '@uw.edu']
    name = get_name(netid)
    rollup_name = get_rollup_name(netid)
    profile.preferred = PreferredNameParts(
        full=name.display_cname,
        first=name.display_fname,
        middle=name.display_mname,
        last=name.display_lname)
    profile.official_name = name.formal_cname
    profile.preferred_name = name.display_cname
    profile.rollup_name = rollup_name.display_cname
    profile.is_profile_admin = GWS().is_profile_admin(netid=netid)
    profile.is_publish_hidden = GWS().is_publish_hidden(netid=netid)
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


def get_rollup_name(netid):
    """
    Look up an irws rollup name by netid. All people should have a name.
    Raise a ServiceError for all no-names.
    """
    name = IRWS().get_name_by_netid(netid, rollup=True)
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
        phone_numbers=[format_phone_number(x) for x in employee.wp_phone],
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
        phone_numbers=[format_phone_number(x) for x in student.wp_phone],
        class_majors=[', '.join(pair) for pair in izip_longest(
            student.wp_title, student.wp_department, fillvalue='-')],
        publish=(False if student.wp_publish == 'N' else True)
    )


def format_phone_number(phone_number):
    """If '+1 xxx xxx-xxxx', format as (xxx) xxx-xxxx, else leave it alone."""
    return re.sub(r'^\+1 (\d{3}) (\d{3}-\d{4})$', r'(\1) \2', phone_number)
