# This class requires the uw's restclients app.  here mainly as an example
# pacakge

from restclients.gws import GWS
import authz_group.models


class UWGroupService():
    def is_member_of_group(self, user_name, group_source_id):
        gws = GWS()
        if gws.is_effective_member(group_source_id, user_name):
            return True
        return False

    def group_display_name(self, source_id):
        return source_id

    def group_membership_url(self, group_source_id):
        return "https://iam-ws.u.washington.edu/group_ws/v1/group/%s/member" % group_source_id

    @staticmethod
    def get_groups_for_user(login_name):
        person = authz_group.models.Person.objects.get(login_name = login_name)

        crowd_owners = authz_group.models.GWSCrowdOwner.objects.filter(person_id = person.pk)

        crowds = []
        for owner in crowd_owners:
            crowds.append(owner.gws_crowd)

        return crowds

    @staticmethod
    def get_source_type():
        return 'Catalyst::Model::GroupSource::GWS'

    @staticmethod
    def get_css_source_type():
        return 'Catalyst--Model--GroupSource--GWS'

    @staticmethod
    def json_data_structure():
        return {
            'source_type': UWGroupService.get_source_type(),
            'display_name': 'UW Groups',
            'css_source_type': UWGroupService.get_css_source_type(),
        }
