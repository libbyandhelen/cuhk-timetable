from django.conf.urls import url

from Course.router import router_course, router_course_id_component, router_course_id_assessment, \
    router_course_id_section, router_course_id_section_id_meeting, router_course_term, router_course_id_section_id

urlpatterns = [
    url(r'^(?P<course_id>\d+)$', router_course),
    url(r'^(?P<course_id>\d+)/components$', router_course_id_component),
    url(r'^(?P<course_id>\d+)/assessments$', router_course_id_assessment),
    url(r'^(?P<course_id>\d+)/sections$', router_course_id_section),
    url(r'^(?P<course_id>\d+)/sections/(?P<section_id>\d+)$', router_course_id_section_id),
    url(r'^(?P<course_id>\d+)/sections/(?P<section_id>\d+)/meetings$', router_course_id_section_id_meeting),
    url(r'^terms$', router_course_term),
]
