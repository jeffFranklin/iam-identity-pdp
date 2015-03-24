"""
This implementation loads groups from django settings.  The structure looks like this:

AUTHZ_GROUP_BACKEND='authz_group.authz_implementation.settings.Settings'

AUTHZ_GROUP_MEMBERS = {
                        "group_name": ["user1", "user2"],
                        "another_group": ["usera", "userb"],
                      }

"""
from django.conf import settings

class Settings():
    def is_member_of_group(self, user_name, group_source_id):
        groups = settings.AUTHZ_GROUP_MEMBERS
        if not group_source_id in groups:
            return False

        members = groups[group_source_id]
        for member in members:
            if user_name == member:
                return True
        return False
