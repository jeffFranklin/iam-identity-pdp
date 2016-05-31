from pdp.models import Profile
try:  # http://asq.googlecode.com/hg-history/1.0/asq/_portability.py
    # Python 2
    from itertools import izip_longest
except ImportError:
    # Python 3
    from itertools import zip_longest as izip_longest


def test_profile():
    dct_in = dict(
        netid='joe',
        preferred_name='Joe',
        official_name='JOE',
        emails=['joe@example.com'],
        student=dict(official_name='JoE', phone_numbers=['1'],
                     class_majors=['Junior, ART'],
                     emails=['j@jstudent.u'],
                     publish=False),
        employee=dict(official_name='jOe', phone_numbers=['2'],
                      emails=['j@j.u'], addresses=['123'], box='456',
                      departments=['3', '4'], titles=['boss', 'employee'],
                      publish='E',
                      ),
        preferred=dict(full='J O E', first='J', middle='O', last='E'),
        is_profile_admin=False,
        is_publish_hidden=False,
        rollup_name=dict(full='Joe Roll', first='J',
                         middle='Roll', last='E'
                         ),
    )
    dct_in['employee']['titledepts'] = [
                    ', '.join(pair) for pair in izip_longest(
                        dct_in['employee']['titles'],
                        dct_in['employee']['departments'],
                        fillvalue='-')]
    dct_out = Profile(**dct_in).to_dict()
    assert dct_in == dct_out
    assert dct_in is not dct_out
