import re

def netid_from_remote_user(remote_user):
    if '@' in remote_user and not remote_user.endswith('@washington.edu'):
        raise ValueError('not a valid remote user')
    return re.sub(r'@washington.edu', '', remote_user)
