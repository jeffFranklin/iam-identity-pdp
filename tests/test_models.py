from pdp.models import BaseModel, Profile
from pytest import mark, raises
try:  # http://asq.googlecode.com/hg-history/1.0/asq/_portability.py
    # Python 2
    from itertools import izip_longest
except ImportError:
    # Python 3
    from itertools import zip_longest as izip_longest


class FooModel(BaseModel):
    netid = None
    sub_foo = None
    _specials = {'sub_foo': 'test_models.FooSubModel'}


class FooSubModel(BaseModel):
    netid = None


def test_base_model_no_dict():
    model = FooModel()
    assert model.netid is None
    assert model.sub_foo is None


def test_base_model_good_dict():
    model = FooModel(netid='joe', sub_foo=dict(netid='blow'))
    assert model.netid == 'joe'
    assert model.sub_foo.netid == 'blow'


def test_base_model_to_dict():
    model = FooModel(netid='joe', sub_foo=dict(netid='blow'))
    assert model.to_dict() == {'netid': 'joe', 'sub_foo': {'netid': 'blow'}}


def test_base_model_to_dict_no_sub():
    model = FooModel(netid='joe')
    assert model.to_dict() == {'netid': 'joe', 'sub_foo': None}


@mark.parametrize('dct', [
    {'netid': 'joe', 'name': 'bad'},
    {'netid': 'joe', 'sub_foo': {'bad': 'bad'}},
    {'netid': 'joe', '_hidden': 'bad'},
    {'netid': 'joe', 'sub_foo': {'_hidden': 'bad'}}],
    ids=['bad attribute', 'bad sub attribute', 'underscore attibute',
         'underscore sub attibute'])
def test_base_model_bad_dict(dct):
    with raises(ValueError):
        FooModel(**dct)


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
        is_publish_hidden=False
    )
    dct_in['employee']['titledepts'] = [
                    ', '.join(pair) for pair in izip_longest(
                        dct_in['employee']['titles'],
                        dct_in['employee']['departments'],
                        fillvalue='-')]
    dct_out = Profile(**dct_in).to_dict()
    assert dct_in == dct_out
    assert dct_in is not dct_out
