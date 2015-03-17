from django.http import HttpResponse
import json
from userservice.user import UserService


class RESTDispatch:
    """
    Handles passing on the request to the correct view
    method based on the request type.
    """
    def run(self, *args, **named_args):
        request = args[0]

        user_service = UserService()
        netid = user_service.get_user()
        if not netid:
            return invalid_session()

        if "GET" == request.META['REQUEST_METHOD']:
            if hasattr(self, "GET"):
                return self.GET(*args, **named_args)
            else:
                return invalid_method()
        elif "POST" == request.META['REQUEST_METHOD']:
            if hasattr(self, "POST"):
                return self.POST(*args, **named_args)
            else:
                return invalid_method()
        elif "PUT" == request.META['REQUEST_METHOD']:
            if hasattr(self, "PUT"):
                return self.PUT(*args, **named_args)
            else:
                return invalid_method()
        elif "DELETE" == request.META['REQUEST_METHOD']:
            if hasattr(self, "DELETE"):
                return self.DELETE(*args, **named_args)
            else:
                return invalid_method()

        else:
            return invalid_method()


# these are called by ajax, so need to be parsable
# login by shib not possible with ajax

def invalid_session():
    return HttpResponse('{"error_message": "session timeout"}',
                                status = 401,
                                content_type='application/json')

def __response_400(msg):
    response = HttpResponse('{"error_message": "%s"}' % (msg));
    response.status_code = 400
    return response

def invalid_arg():
    return __response_400('No valid argument')

def data_not_found():
    return __response_400('Data not found')

def invalid_method():
    return __response_400("Method not allowed")

