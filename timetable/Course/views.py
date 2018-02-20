from django.shortcuts import render

from Course.models import Course, Component, Assessment
from base.decorator import require_get, require_login
from base.error import Error
from base.response import error_response, response


@require_get
@require_login
def get_course_info(request, course_id):
    """GET /api/courses/:course_id"""
    ret = Course.get_course_by_id(course_id)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_course = ret.body
    return response(body=o_course.to_dict())


@require_get
@require_login
def get_components_by_course(request, course_id):
    """GET /api/courses/:course_id/components"""
    ret = Course.get_course_by_id(course_id)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_course = ret.body

    ret = Component.get_component_by_course(o_course)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    components = ret.body

    component_list = []
    for component in components:
        component_list.append(component.to_dict())
    return response(body=component_list)


@require_get
@require_login
def get_assessments_by_course(request, course_id):
    """GET /api/courses/:course_id/assessments"""
    ret = Course.get_course_by_id(course_id)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_course = ret.body

    ret = Assessment.get_assessment_by_course(o_course)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    assessments = ret.body

    assessment_list = []
    for assessment in assessments:
        assessment_list.append(assessment.to_dict())
    return response(body=assessment_list)
