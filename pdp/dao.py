from pdp.models import Profile, PreferredNameParts
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
