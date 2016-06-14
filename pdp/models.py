from idbase.models import BaseModel


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
    rollup_name = None
    is_profile_admin = False
    is_publish_hidden = False


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
    publish = False  # True/False, default false


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
