
import json

from django.http import HttpResponse

from base.error import Error


class Ret:
    """Ret class, used for almost every methods' return package"""
    def __init__(self, error=Error.OK, body=None):
        """init constructor"""
        self.error = error
        self.body = body or []


def response(code=0, msg="ok", body=None):
    """return HttpResponse, used for every api dealing functions"""
    resp = {
        "code": code,
        "msg": msg,
        "body": body or [],
    }

    http_resp = HttpResponse(
        json.dumps(resp, ensure_ascii=False),
        status=200,
        content_type="application/json; encoding=utf-8",
    )
    return http_resp


def error_response(error_id, append_msg=""):
    """return HttpResponse with error"""
    for error in Error.ERROR_TUPLE:
        if error_id == error[0]:
            return response(code=error_id, msg=error[1]+append_msg)
    return error_response(Error.NOT_FOUND_ERROR)