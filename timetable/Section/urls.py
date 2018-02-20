from django.conf.urls import url

from Section.router import router_selectsection, router_selectsection_id, router_selectsection_color

urlpatterns = [
    url(r'^$', router_selectsection),
    # url(r'^color$', router_selectsection_color),
    url(r'^(?P<section_id>\d+)$', router_selectsection_id),
    url(r'^color$', router_selectsection_color)
]
