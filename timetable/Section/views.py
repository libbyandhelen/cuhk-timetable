import random

from django.shortcuts import render

from Course.models import Course
from Section.models import Section, Meeting, SelectSection
from base.common import get_user_from_session
from base.decorator import require_get, require_login, require_post, require_json, require_params, require_delete
from base.error import Error
from base.response import error_response, response


@require_get
@require_login
def get_terms(request):
    """GET /api/courses/terms"""
    ret = Section.get_terms()
    if ret.error is not Error.OK:
        return error_response(ret.error)
    terms = ret.body
    return response(body=terms)


@require_login
@require_get
def get_sections_by_course(request, course_id):
    """GET /api/courses/:course_id/sections"""
    ret = Course.get_course_by_id(course_id)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_course = ret.body

    ret = Section.get_sections_by_course(o_course)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    sections = ret.body

    section_list = []
    for section in sections:
        section_list.append(section.to_dict())
    return response(body=section_list)


@require_login
@require_post
@require_json
@require_params(['category', 'term', 'type', 'section_id'])
def get_sibling_sections(request, course_id):
    """POST /api/courses/:course:id/sections"""
    category = request.POST['category']
    term = request.POST['term']
    type = request.POST['type']
    section_id = request.POST['section_id']

    ret = Course.get_course_by_id(course_id)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_course = ret.body

    ret = Section.get_sections_by_course(o_course)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    sections = ret.body

    section_list = []
    for section in sections:
        if section.category == category and section.term == term and section.type == type and section.id != section_id:
            section_list.append(dict(
                sibling=section.to_dict(),
                self_id=section_id,
            ))
    return response(body=section_list)


@require_login
@require_get
def get_section(request, course_id, section_id):
    """GET /api/courses/:course_id/sections/:section_id"""
    ret = Course.get_course_by_id(course_id)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_course = ret.body

    ret = Section.get_section_by_id(section_id)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_section = ret.body

    ret = o_section.belong_to(o_course)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    return response(body=o_section)


@require_login
@require_get
def get_meetings_by_section(request, course_id, section_id):
    """GET /api/courses/:course_id/sections/:section_id/meetings"""
    ret = Course.get_course_by_id(course_id)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_course = ret.body

    ret = Section.get_section_by_id(section_id)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_section = ret.body

    ret = o_section.belong_to(o_course)
    if ret.error is not Error.OK:
        return error_response(ret.error)

    ret = Meeting.get_meetings_by_section(o_section)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    meetings = ret.body

    meeting_list = []
    for meeting in meetings:
        meeting_list.append(meeting.to_dict())
    return response(body=meeting_list)


@require_login
@require_get
def get_selected_sections_by_user(request):
    """GET /api/selectsections"""
    ret = get_user_from_session(request)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_user = ret.body

    ret = SelectSection.get_selected_section_by_user(o_user)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    select_sections = ret.body

    section_list = []
    for select_section in select_sections:
        section_list.append(select_section.to_dict())
    return response(body=section_list)


@require_login
@require_delete
@require_json
@require_params(['course_id', 'category', 'term'])
def delete_section_by_category(request):
    """DELETE /api/selectsections"""
    course_id = request.POST['course_id']
    category = request.POST['category']
    term = request.POST['term']

    ret = get_user_from_session(request)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_user = ret.body

    ret = Course.get_course_by_id(course_id)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_course = ret.body

    ret = SelectSection.get_selected_section_by_user(o_user)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    select_sections = ret.body

    for select_section in select_sections:
        if select_section.section.course == o_course and select_section.section.category == category and select_section.section.term == term:
            select_section.delete()
    return response()


@require_login
@require_post
@require_json
@require_params(['course_id', 'category', 'term'])
def create_select_section(request):
    """POST /api/selectsections"""
    color_scheme = [
        {
            'bgcolor': "#A3E7FC",
            'color': 'black'
        },
        {
            'bgcolor': "#3F7CAC",
            'color': 'white'
        },
        {
            'bgcolor': "#439A86",
            'color': 'white'
        },
        {
            'bgcolor': "#E25186",
            'color': 'white'
        },
        {
            'bgcolor': "#F9DC5C",
            'color': 'black'
        },
        {
            'bgcolor': "#ECCBD9",
            'color': 'black'
        },
        {
            'bgcolor': "#392B58",
            'color': 'white'
        },
        {
            'bgcolor': "#FAC9B8",
            'color': 'black'
        },
        {
            'bgcolor': "#D3F8E2",
            'color': 'balck'
        },
        {
            'bgcolor': "#004E64",
            'color': 'white'
        },
        {
            'bgcolor': "#8CB369",
            'color': 'black'
        }
    ]
    course_id = request.POST['course_id']
    category = request.POST['category']
    term = request.POST['term']

    ret = get_user_from_session(request)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_user = ret.body

    ret = Course.get_course_by_id(course_id)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_course = ret.body

    ret = Section.get_sections_by_course(o_course)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    sections = ret.body

    select_section_list = []
    type_list = []
    for o_section in sections:
        if o_section.category == category and o_section.term == term and o_section.type not in type_list:
            type_list.append(o_section.type)

            ret = SelectSection.get_selected_section_by_details(
                o_user,
                o_course,
                term,
                category,
            )
            if ret.error is not Error.OK:
                return error_response(ret.error)
            same_color = ret.body
            if same_color:
                bgcolor = same_color[0].bgcolor
                color = same_color[0].color
            else:
                rand = random.randint(0, len(color_scheme) - 1)
                bgcolor = color_scheme[rand]['bgcolor']
                color = color_scheme[rand]['color']

            ret = SelectSection.select_section(
                o_user=o_user,
                o_section=o_section,
                bgcolor=bgcolor,
                color=color,
            )
            if ret.error is not Error.OK:
                return error_response(ret.error)
            select_section_list.append(ret.body.to_dict())

    return response(body=select_section_list)


@require_login
@require_delete
def delete_select_section(request, section_id):
    """DELETE /api/selectsections/:section_id"""
    ret = get_user_from_session(request)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_user = ret.body

    ret = Section.get_section_by_id(section_id)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_section = ret.body

    ret = SelectSection.get_select_section(o_user, o_section)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_select_section = ret.body
    o_select_section.delete()
    return response()


@require_login
@require_post
@require_json
@require_params(['bg_color', 'color'])
def create_select_section_by_section_id(request, section_id):
    """POST /api/selectsections/:section_id"""
    bg_color = request.POST['bg_color']
    color = request.POST['color']
    # section_id = request.POST['section_id']

    ret = get_user_from_session(request)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_user = ret.body

    ret = Section.get_section_by_id(section_id)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_section = ret.body

    ret = SelectSection.select_section(o_user, o_section, bg_color, color)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_select_section = ret.body
    return response(body=o_select_section.to_dict())


@require_login
@require_post
@require_json
@require_params(['course_id', 'category', 'term', 'color', 'bg_color'])
def change_color_by_category(request):
    course_id = request.POST['course_id']
    category = request.POST['category']
    color = request.POST['color']
    bg_color = request.POST['bg_color']
    term = request.POST['term']

    ret = get_user_from_session(request)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_user = ret.body

    ret = Course.get_course_by_id(course_id)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    o_course = ret.body

    ret = SelectSection.get_selected_section_by_user(o_user)
    if ret.error is not Error.OK:
        return error_response(ret.error)
    select_sections = ret.body

    select_section_list = []
    for select_section in select_sections:
        if select_section.section.course == o_course and select_section.section.category == category and select_section.section.term == term:
            select_section.bgcolor = bg_color
            select_section.color = color
            select_section.save()
            select_section_list.append(select_section.to_dict())

    return response(body=select_section_list)
