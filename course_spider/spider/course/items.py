# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem

# from Course.models import Course
from Course.models import Course, Component, Assessment
from Section.models import Section, Meeting


class CourseItem(DjangoItem):
    django_model = Course


class ComponentItem(DjangoItem):
    django_model = Component


class AssessmentItem(DjangoItem):
    django_model = Assessment


class SectionItem(DjangoItem):
    django_model = Section


class MeetingItem(DjangoItem):
    django_model = Meeting
