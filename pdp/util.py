import re
from restclients.irws import IRWS


def netid_from_remote_user(remote_user):
    if '@' in remote_user and not remote_user.endswith('@washington.edu'):
        raise ValueError('not a valid remote user')
    return re.sub(r'@washington.edu', '', remote_user)


def get_full_name(request):
    name = IRWS().get_name_by_netid(request.user.netid)
    return full_name_from_object(name)


def full_name_from_object(name):
    parts = ['fname', 'mname', 'lname']
    display = ' '.join([getattr(name, 'display_' + part)
                        for part in parts
                        if getattr(name, 'display_' + part, False)])
    formal = ' '.join([getattr(name, 'formal_' + part)
                       for part in parts
                       if getattr(name, 'formal_' + part, False)])
    return display if display else formal
