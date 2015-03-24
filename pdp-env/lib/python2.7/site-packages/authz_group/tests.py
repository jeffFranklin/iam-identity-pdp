from django.test import TestCase
from django.conf import settings 
from authz_group import Group

class TestAllOK(TestCase):
    def test_ok(self):
        with self.settings(
            AUTHZ_GROUP_BACKEND='authz_group.authz_implementation.all_ok.AllOK'
            ):
            self.assertTrue(Group().is_member_of_group("anyone", "anygroup"))

class TestAllFail(TestCase):
    def test_fail(self):
        with self.settings(
            AUTHZ_GROUP_BACKEND='authz_group.authz_implementation.all_fail.AllFail'
            ):
            self.assertFalse(Group().is_member_of_group("anyone", "anygroup"))

class TestSettingsGroup(TestCase):
    def test_group(self):
        with self.settings(
            AUTHZ_GROUP_BACKEND='authz_group.authz_implementation.settings.Settings',
            AUTHZ_GROUP_MEMBERS={ "test_group": ["test_user1", "test_user2"] }
            ):
            self.assertTrue(Group().is_member_of_group("test_user1", "test_group"))
            self.assertTrue(Group().is_member_of_group("test_user2", "test_group"))
            self.assertFalse(Group().is_member_of_group("test_user3", "test_group"))
            self.assertFalse(Group().is_member_of_group("test_user1", "fake_group"))

