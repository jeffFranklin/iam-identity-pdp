# simple remote_user login

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


class FoxsUserBackend(ModelBackend):

    def authenticate(self, remote_user):
        print '>> my authn: ' + remote_user
        try:
            user = User.objects.get(username=remote_user)
            return user
        except User.DoesNotExist:
            # create missing users
            print 'creating user entery'
            user = User(username=remote_user, password='z')
            user.save()
            return user

    def get_user(self, id):
        print '>> my get_user:'
        user = User.objects.get(pk=id)
        return user
