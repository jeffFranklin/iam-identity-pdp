import re

def is_email(username):
    error_msg = "No override user supplied, please enter a user to override as in the format of an email address"
    if len(username) > 0:
        match = re.match('[^@]+@[^@]+\.[^@]+', username)
        if not match:
            error_msg = "Override user must be an email address.  You entered: "
        else:
            error_msg = None
    return error_msg
