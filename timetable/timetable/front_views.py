from django.shortcuts import render

from Course.models import Course, Assessment, Component
from Section.models import Section, Meeting
from base.common import get_user_from_session
from base.decorator import require_login
from base.error import Error
from base.response import error_response


@require_login
def timetable_page(request):
    return render(request, 'index.html')


def signup_page(request):
    return render(request, 'signup.html')


@require_login
def courses_page(request, course_id):
    ret = get_user_from_session(request)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_user = ret.body

    ret = Course.get_course_by_id(course_id)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_course = ret.body

    return render(request, 'courses.html', dict(
        course_id=o_course.id
    ))
