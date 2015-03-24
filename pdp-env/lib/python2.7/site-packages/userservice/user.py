from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth.models import User
import logging

from threading import currentThread

class UserService:
    _user_data = {}
    logger = logging.getLogger(__name__)

    def _get_current_user_data(self):
        thread_id = currentThread()
        if not UserService._user_data:
            return {}
        if thread_id in UserService._user_data:
            return UserService._user_data[currentThread()]
        return {}

    def _require_middleware(self):
        if not "initialized" in self._get_current_user_data():
            print "You need to have this line in your MIDDLEWARE_CLASSES:"
            print "'userservice.user.UserServiceMiddleware',"

            raise Exception("You need the UserServiceMiddleware")

    def get_user(self):
        self._require_middleware()

        override = self.get_override_user()
        if override and len(override) > 0:
            return override

        actual = self.get_original_user()
        if not actual or len(actual) == 0:
            return None
        return actual

    def get_acting_user(self):
        self._require_middleware()
        actual = self.get_original_user()
        if not actual or len(actual) > 0:
            return actual

        override = self.get_override_user()
        if override and len(override) == 0:
            return None
        return override

    def get_original_user(self):
        user_data = self._get_current_user_data()
        if "original_user" in user_data:
            return user_data["original_user"]

    def get_override_user(self):
        user_data = self._get_current_user_data()
        if "override_user" in user_data:
            return user_data["override_user"]

    def set_user(self, user):
        user_data = self._get_current_user_data()
        user_data["original_user"] = user
        user_data["session"]["_us_user"] = user

    def set_override_user(self, override):
        user_data = self._get_current_user_data()
        user_data["override_user"] = override
        user_data["session"]["_us_override"] = override

    def clear_override(self):
        user_data = self._get_current_user_data()
        user_data["override_user"] = None
        user_data["session"]["_us_override"] = None


class UserServiceMiddleware(object):

    logger = logging.getLogger(__name__)

    def process_request(self, request):
        thread = currentThread()
        UserService._user_data[thread] = {}
        UserService._user_data[thread]["initialized"] = True

        session = request.session
        UserService._user_data[thread]["session"] = session

        if not "_us_user" in session:
            user = self._get_authenticated_user(request)
            if user:
                UserService._user_data[thread]["original_user"] = user
                UserService._user_data[thread]["session"]["_us_user"] = user
        else:
            UserService._user_data[thread]["original_user"] = session["_us_user"]

        if "_us_override" in session:
            UserService._user_data[thread]["override_user"] = session["_us_override"]

        username = UserService().get_user()
        if username:
            new_user, created = User.objects.get_or_create(username=username)
            request.user = new_user

    def process_response(self, request, response):
        thread = currentThread()
        UserService._user_data[thread] = {}
        return response

    def _get_authenticated_user(self, request):
        netid = None
        if settings.DEBUG:
            if request.user.username:
                netid = request.user.username
            else:
                if hasattr(settings, "USER_SERVICE_NO_DEFAULT_USER"):
                    return None
                netid = 'javerage'
        else:
            netid = request.user.username

        return netid


