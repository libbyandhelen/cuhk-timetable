
"""provide decodators, for api method validation"""
import json
from functools import wraps

from base.common import get_user_from_session
from base.error import Error
from base.response import error_response


def require_get(func):
    """api require get method"""
    def wrapper(request, *args, **kwargs):
        """decorator declaration, get func params to validate"""
        if request.method == "GET":
            return func(request, *args, **kwargs)
        return error_response(Error.ERROR_METHOD)
    return wrapper


def require_post(func):
    """api require post method"""
    def wrapper(request, *args, **kwargs):
        """decorator declaration, get func params to validate"""
        if request.method == "POST":
            return func(request, *args, **kwargs)
        return error_response(Error.ERROR_METHOD)
    return wrapper


def require_put(func):
    """api require put method"""
    def wrapper(request, *args, **kwargs):
        """decorator declaration, get func params to validate"""
        if request.method == "PUT":
            return func(request, *args, **kwargs)
        return error_response(Error.ERROR_METHOD)
    return wrapper


def require_delete(func):
    """api require delete method"""
    def wrapper(request, *args, **kwargs):
        """decorator declaration, get func params to validate"""
        if request.method == "DELETE":
            return func(request, *args, **kwargs)
        return error_response(Error.ERROR_METHOD)
    return wrapper


def require_params(r_params):
    """params validation"""
    def decorator(func):
        """decorator"""
        def wrapper(request, *args, **kwargs):
            """decorator declaration, get func params to validate"""
            for require_param in r_params:
                if require_param not in request.POST:
                    return error_response(Error.REQUIRE_PARAM,
                                          append_msg=require_param)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_get_params(r_params):
    """params validation for GET method"""
    def decorator(func):
        """decorator"""
        def wrapper(request, *args, **kwargs):
            """decorator declaration, get func params to validate"""
            for require_param in r_params:
                if require_param not in request.GET:
                    return error_response(Error.REQUIRE_PARAM,
                                          append_msg=require_param)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_json(func):
    """require json data for request"""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        """decorator declaration, get func params to validate"""
        if request.body:
            try:
                request.POST = json.loads(request.body.decode())
            except json.JSONDecodeError as err:
                print(str(err))
            return func(request, *args, **kwargs)
        return error_response(Error.REQUIRE_JSON)
    return wrapper


def require_login(func):
    def wrapper(request, *args, **kwargs):
        ret = get_user_from_session(request)
        if ret.error is not Error.OK:
            return error_response(ret.error)
        return func(request, *args, **kwargs)
    return wrapper


# def decorator_generator(verify_func, error_id):
#     """generate decorators, like require_login"""
#     def decorator(func):
#         """decorator"""
#         def wrapper(request, *args, **kwargs):
#             """decorator declaration, get func params to validate"""
#             if verify_func(request):
#                 return func(request, *args, **kwargs)
#             return error_response(error_id)
#         return wrapper
#     return decorator
#
#
# def require_login_func(request):
#     """check if login"""
#     o_user = get_user_from_session(request)
#     return o_user is not None
#
# require_login = decorator_generator(require_login_func, Error.REQUIRE_LOGIN)
