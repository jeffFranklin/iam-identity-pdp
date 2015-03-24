from django.db import models
from wsgiref.handlers import format_date_time
import time
from authz_group.authz_implementation.solstice import SolsticeCrowdImplementation
from django.conf import settings

class Person(models.Model):
    person_id = models.AutoField(primary_key = True, db_column = 'person_id')
    login_name = models.TextField(max_length=128, db_column='login_name')
    name = models.TextField(max_length=255, db_column='name')

    # This is a shim for an approach to handle scoped login names.
    # If you had joe@google.com, and joe@yahoo.com, google.com could be
    # login_realm:1, and yahoo.com login_realm:2, so the users would be stored
    # as (joe, 1) and (joe, 2)
    # This was done as an easy way to separate privileges by where a person is
    # from.
    login_realm_id = models.IntegerField(db_column='login_realm_id', default=1)

    class Meta:
        db_table = 'Person'

class Crowd(models.Model):
    id = models.AutoField(primary_key = True, db_column = 'group_id')
    source_key = models.CharField(max_length = 100, db_column = 'source_key', db_index=True)
    source_type = models.CharField(max_length = 100, db_column = 'model_package')

    owners = models.ManyToManyField(Person, through='CrowdOwner')

    _source_types = {}

    def get_group(self):
        if self._group:
            return self._group

        raise Exception("Not implemented!")


    def is_member(self, login_name):
        backend = self.get_backend_for_source(self.source_type)

        return backend().is_member_of_group(login_name, self.source_key)

    def json_data_structure(self):
        css_source_type = self.source_type.replace(':', '-')

        data = {
            'id': self.id,
            'source_key': self.source_key,
            'source_type': self.source_type,
            'css_source_type': css_source_type,
            'implementation': [],
        }

        group = self.get_group()
        if (hasattr(group, 'json_data_structure')):
            data["implementation"] = group.json_data_structure()

        return data

    @staticmethod
    def get_crowds_for_user(login_name):
        all_groups = []
        for implementation in Crowd.get_crowd_backends():
            impl_groups = implementation.get_groups_for_user(login_name)
            all_groups.extend(impl_groups)

        return Crowd.wrap_implementations_in_crowds(all_groups)

    @staticmethod
    def get_crowd_backends():
        # XXX
        if hasattr(settings, 'AUTHZ_GROUP_CROWD_IMPLEMENTATIONS'):
            pass

        return [SolsticeCrowdImplementation]


    @staticmethod
    def wrap_implementations_in_crowds(implementation_groups):
        wrapped = []
        for group in implementation_groups:
            wrapped.append(Crowd._wrap_group(group))

        return wrapped

    @staticmethod
    def _wrap_group(group):
        crowd, created = Crowd.objects.get_or_create(source_key = group.id, source_type = group.get_source_type())
        crowd._group = group

        return crowd

    @staticmethod
    def register_source_types():
        for backend in Crowd.get_crowd_backends():
            Crowd._source_types[backend.get_source_type()] = backend

    @staticmethod
    def get_backend_for_source(source_type):
        if source_type in Crowd._source_types:
            return Crowd._source_types[source_type]

        raise UnknownCrowdBackendException(source_type)

    class Meta:
        db_table = 'GroupWrapper'
        unique_together = ('source_key', 'source_type')

class UnknownCrowdBackendException(Exception):
    pass

Crowd.register_source_types()

class CrowdOwner(models.Model):
    id = models.AutoField(db_column='group_owner_id', primary_key=True)
    group = models.ForeignKey(Crowd, db_column='group_id')
    person = models.ForeignKey(Person, db_column='person_id', db_index=True)

    class Meta:
        db_table = 'GroupOwner'
        unique_together = ('group', 'person')


# This is supporting the solstice authz_implemention
class SolsticeCrowd(models.Model):
    id = models.AutoField(db_column='source_key', primary_key=True)
    creator = models.ForeignKey(Person, db_column='creator_id', related_name='creator_person')
    application = models.CharField(max_length=255, db_column='application')
    is_visible = models.BooleanField(db_column='is_visible')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(db_column='description')
    date_created = models.DateTimeField(db_column='date_created')
    date_modified = models.DateTimeField(db_column='date_modified')
    member_string = models.CharField(max_length=255, db_column='member_str')

    owners = models.ManyToManyField(Person, through='SolsticeCrowdOwner', related_name='sol_crowd_owner')

    def json_data_structure(self):
        return {
            'name': self.name,
            'description': self.description,
            'date_modified': format_date_time(time.mktime(self.date_modified.timetuple())),
            'date_created': format_date_time(time.mktime(self.date_created.timetuple())),
            'member_string': self.member_string,
        }

    def get_source_type(self):
        return SolsticeCrowdImplementation.get_source_type()

    class Meta:
        db_table = 'Crowd'

class SolsticeCrowdMember(models.Model):
    sol_crowd = models.ForeignKey(SolsticeCrowd, db_column='crowd_id', db_index=True)
    person = models.ForeignKey(Person, db_column='person_id', db_index=True)

    class Meta:
        db_table = 'PeopleInCrowd'
        unique_together = ('sol_crowd', 'person')

class SolsticeCrowdOwner(models.Model):
    id = models.AutoField(db_column='crowd_owner_id', primary_key=True)
    sol_crowd = models.ForeignKey(SolsticeCrowd, db_column='crowd_id')
    person = models.ForeignKey(Person, db_column='person_id', db_index=True)

    class Meta:
        db_table = 'CrowdOwner'
        unique_together = ('sol_crowd', 'person')


# This is supporting the uw_group_service authz_implemention
class GWSCrowd(models.Model):
    id = models.IntegerField(db_column='id')
    source_key = models.CharField(db_column='source_key', primary_key=True, max_length=255)
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(db_column='description')
    date_created = models.DateTimeField(db_column='date_created')
    date_modified = models.DateTimeField(db_column='date_modified')
    date_reconciled = models.DateTimeField(db_column='date_reconciled')

    def json_data_structure(self):
        return {
            'name': self.name,
            'description': self.description,
            'date_modified': format_date_time(time.mktime(self.date_modified.timetuple())),
            'date_created': format_date_time(time.mktime(self.date_created.timetuple())),
        }

    def get_source_type(self):
        return UWGroupService.get_source_type()

    class Meta:
        db_table = 'GWSGroup'

class GWSCrowdOwner(models.Model):
    id = models.AutoField(db_column='gws_viewers_id', primary_key=True)
    gws_crowd = models.ForeignKey(GWSCrowd, db_column='source_key')
    person_id = models.IntegerField(db_column='person_id', db_index=True)

    class Meta:
        db_table = 'GWSViewers'
        unique_together = ('gws_crowd', 'person_id')





