from pdp.models import Profile


def get_profile(netid):
    """Return the profile for a given netid."""
    fake_profile = dict(
        netid=netid,
        preferred_name='Timmy Johnson',
        official_name='TIMOTHY ROBERT JOHNSON',
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
    return Profile(dct=fake_profile)
