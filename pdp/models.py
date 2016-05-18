from importlib import import_module


class BaseModel(object):
    _specials = {}

    def __init__(self, **kwargs):
        """
        Initialize instance attributes to those of the class attributes
        unless overridden in kwargs. _specials is a dictionary of
        attribute name to BaseModel class.
        """
        bad_keys = (set(kwargs.keys()) - set(vars(self.__class__).keys()) or
                    [x for x in kwargs.keys() if x.startswith('_')])
        if bad_keys:
            raise ValueError('Bad value in dictionary: {}'.format(bad_keys))
        for key in (x for x in vars(self.__class__).keys()
                    if not x.startswith('_')):
            specials = getattr(self.__class__, '_specials', {})
            if key in specials and key in kwargs:
                module, attr = specials[key].rsplit('.', 1)
                subobj = getattr(import_module(module), attr)(**kwargs[key])
                setattr(self, key, subobj)
            elif key in kwargs:
                setattr(self, key, kwargs[key])
            else:
                setattr(self, key, getattr(self.__class__, key))

    def to_dict(self):
        """Return a dictionary representation of a model object."""
        ret = {}
        for att in (x for x in vars(self) if not x.startswith('_')):
            specials = self.__class__._specials
            if att in specials and getattr(self, att):
                ret[att] = getattr(self, att).to_dict()
            else:
                ret[att] = getattr(self, att)
        return ret


class Profile(BaseModel):
    _specials = {
        'student': 'pdp.models.StudentProfile',
        'employee': 'pdp.models.EmployeeProfile',
        'preferred': 'pdp.models.PreferredNameParts'
    }
    netid = None
    official_name = None
    emails = []
    student = None
    employee = None
    preferred_name = None
    preferred = None
    is_profile_admin = False


class PreferredNameParts(BaseModel):
    full = ''
    first = ''
    middle = ''
    last = ''


class StudentProfile(BaseModel):
    official_name = None
    phone_numbers = []
    class_majors = []  # A join of year list and majors list
    emails = []
    publish = True  # True/False, default true


class EmployeeProfile(BaseModel):
    official_name = None
    phone_numbers = []
    emails = []
    addresses = []
    departments = []
    titles = []
    box = None
    titledepts = []  # Title and Department join
    publish = 'Y'
