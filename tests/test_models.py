from pdp.models import BaseModel, Profile
from pytest import mark, raises


class FooModel(BaseModel):
    def __init__(self, dct={}):
        self.netid = None
        self.sub_foo = None
        self._specials = {'sub_foo': FooSubModel}
        super(self.__class__, self).__init__(dct=dct)


class FooSubModel(BaseModel):
    def __init__(self, dct={}):
        self.netid = None
        super(self.__class__, self).__init__(dct=dct)


def test_base_model_no_dict():
    model = FooModel()
    assert model.netid is None
    assert model.sub_foo is None


def test_base_model_good_dict():
    model = FooModel(dct=dict(netid='joe', sub_foo=dict(netid='blow')))
    assert model.netid == 'joe'
    assert model.sub_foo.netid == 'blow'


def test_base_model_to_dict():
    model = FooModel(dct=dict(netid='joe', sub_foo=dict(netid='blow')))
    assert model.to_dict() == {'netid': 'joe', 'sub_foo': {'netid': 'blow'}}


def test_base_model_to_dict_no_sub():
    model = FooModel(dct=dict(netid='joe'))
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
        FooModel(dct=dct)


def test_profile():
    dct_in = dict(
        netid='joe',
        preferred_name='Joe',
        official_name='JOE',
        emails=['joe@example.com'],
        student=dict(official_name='JoE', phone_numbers=['1'], clazz='Junior',
                     majors=['ART'], system_key='009123456',
                     emails=['j@jstudent.u']),
        employee=dict(official_name='jOe', phone_numbers=['2'],
                      emails=['j@j.u'], address='123', box='456',
                      departments=['3', '4'], titles=['boss', 'employee']),
        preferred=dict(full='J O E', first='J', middle='O', last='E')
    )
    dct_out = Profile(dct=dct_in).to_dict()
    assert dct_in == dct_out
    assert dct_in is not dct_out
