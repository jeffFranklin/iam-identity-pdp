class BaseModel(object):
    _specials = {}

    def __init__(self, dct={}):
        bad_keys = (set(dct.keys()) - set(vars(self).keys()) or
                    [x for x in dct.keys() if x.startswith('_')])
        if bad_keys:
            raise ValueError('Bad value in dictionary: {}'.format(bad_keys))
        for key in (x for x in dct.keys() if hasattr(self, x)):
            if dct.get(key) and key in getattr(self, '_specials', {}):
                setattr(self, key, self._specials[key](dct[key]))
            else:
                setattr(self, key, dct[key])

    def to_dict(self):
        ret = {}
        for att in (x for x in vars(self).keys()if not x.startswith('_')):
            if (att in self._specials and
                    getattr(self, att) and
                    hasattr(self._specials[att], 'to_dict')):
                ret[att] = getattr(self, att).to_dict()
            else:
                ret[att] = getattr(self, att)
        return ret


class Profile(BaseModel):
    def __init__(self, dct={}):
        self._specials = {
            'student': StudentProfile,
            'employee': EmployeeProfile,
            'preferred': PreferredNameParts
        }
        self.netid = None
        self.official_name = None
        self.emails = []
        self.student = None
        self.employee = None
        self.preferred_name = None
        self.preferred = None
        super(self.__class__, self).__init__(dct=dct)


class PreferredNameParts(BaseModel):
    def __init__(self, dct={}):
        self.full = ''
        self.first = ''
        self.middle = ''
        self.last = ''
        super(self.__class__, self).__init__(dct=dct)


class StudentProfile(BaseModel):
    def __init__(self, dct={}):
        self.system_key = None
        self.official_name = None
        self.phone_numbers = []
        self.clazz = None
        self.majors = []
        self.emails = []
        super(self.__class__, self).__init__(dct=dct)


class EmployeeProfile(BaseModel):
    def __init__(self, dct={}):
        self.official_name = None
        self.phone_numbers = []
        self.emails = []
        self.addresses = []
        self.departments = []
        self.titles = []
        self.box = None
        self.titledepts = []  # Title and Department join

        super(self.__class__, self).__init__(dct=dct)
