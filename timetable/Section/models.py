from django.db import models

from Course.models import Course
from User.models import User
from base.error import Error
from base.response import Ret


class Section(models.Model):
    L = {
        'section_code': 32,
        'term': 32,
        'type': 32,
        'status': 32,
        'instruction_mode': 32,
        'instructor': 32,
        'language': 32,
        'category': 32,
    }

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )

    section_code = models.CharField(
        max_length=L['section_code']
    )
    category = models.CharField(
        max_length=L['category']
    )
    term = models.CharField(
        max_length=L['term']
    )
    type = models.CharField(
        max_length=L['type']
    )
    status = models.CharField(
        max_length=L['status']
    )
    instruction_mode = models.CharField(
        max_length=L['instruction_mode']
    )
    instructor = models.CharField(
        max_length=L['instructor']
    )
    language = models.CharField(
        max_length=L['language']
    )
    class_capacity = models.IntegerField(
    )
    enrollment_total = models.IntegerField()
    available_seat = models.IntegerField()
    wait_capacity = models.IntegerField()
    wait_total = models.IntegerField()

    def __str__(self):
        return str(self.id) + "  " + str(self.course.course_code) + ' - ' + str(self.section_code)

    @staticmethod
    def get_section_by_id(section_id):
        try:
            o_section = Section.objects.get(id=section_id)
        except Section.DoesNotExist:
            return Ret(Error.SECTION_NOT_EXIST)
        return Ret(Error.OK, body=o_section)

    @staticmethod
    def get_terms():
        terms = []
        sections = Section.objects.all()
        for section in sections:
            if section.term not in terms:
                terms.append(section.term)

        return Ret(Error.OK, body=terms)

    # get all sections of a course
    @staticmethod
    def get_sections_by_course(o_course):
        sections = Section.objects.filter(course=o_course)
        return Ret(Error.OK, sections)

    @staticmethod
    def get_sections_for_spider(course_code, term, section_code):
        ret = Course.get_course_by_code(course_code)
        if ret.error is not Error.OK:
            return Ret(ret.error)
        o_course = ret.body

        ret = Section.get_sections_by_course(o_course)
        if ret.error is not Error.OK:
            return Ret(ret.error)
        sections = ret.body

        for section in sections:
            if section.term == term and section.section_code == section_code:
                return Ret(body=section)
        return Ret(Error.SECTION_NOT_EXIST)

    def to_dict(self):
        ret = Meeting.get_meetings_by_section(self)
        if ret.error is not Error.OK:
            return Ret(ret.error)
        meetings = ret.body

        meeting_list = []
        for meeting in meetings:
            meeting_list.append(meeting.to_dict())

        return dict(
            id=self.id,
            # course_id=self.course_id,
            # course_code=self.course.course_code,
            course=self.course.to_dict(),
            section_code=self.section_code,
            category=self.category,
            term=self.term,
            type=self.type,
            status=self.status,
            instruction_mode=self.instruction_mode,
            instructor=self.instructor,
            language=self.language,
            class_capacity=self.class_capacity,
            enrollment_total=self.enrollment_total,
            available_seat=self.available_seat,
            wait_capacity=self.wait_capacity,
            wait_total=self.wait_total,
            meetings=meeting_list,
        )

    def belong_to(self, o_course):
        if self.course == o_course:
            return Ret(Error.OK)
        return Ret(Error.SECTION_NOT_BELONG_TO_COURSE)


class SelectSection(models.Model):
    L = {
        'bgcolor': 10,
        'color': 10,
    }
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE
    )

    bgcolor = models.CharField(
        max_length=L['bgcolor'],
        default='',
        null=True,

    )

    color = models.CharField(
        max_length=L['color'],
        default='',
        null=True,
    )

    def __str__(self):
        return 'user: {} - cousre: {} section: {} - color: {}' \
            .format(self.user_id, self.section.course.course_code, self.section.section_code, self.bgcolor)

    @classmethod
    def create(cls, o_user, o_section, bgcolor, color):
        try:
            o_select_section = cls(
                user=o_user,
                section=o_section,
                bgcolor=bgcolor,
                color=color,
            )
            o_select_section.save()
        except:
            return Ret(Error.ERROR_CREATE_SELECTSECTION)
        return Ret(Error.OK, o_select_section)

    @staticmethod
    def get_select_section_by_id(select_section_id):
        try:
            o_select_section = SelectSection.objects.get(id=select_section_id)
        except SelectSection.DoesNotExist:
            return Ret(Error.SELECT_SECTION_NOT_EXIST)
        return Ret(Error.OK, body=o_select_section)

    # get all the sections selected by the user
    @staticmethod
    def get_selected_section_by_user(o_user):
        select_sections = SelectSection.objects.filter(user=o_user)
        # sections = []
        # for select_section in select_sections:
        #     sections.append(select_section.section)

        return Ret(Error.OK, select_sections)

    @staticmethod
    def get_selected_section_by_details(o_user, o_course, term, category):
        ret = SelectSection.get_selected_section_by_user(o_user)
        if ret.error is not Error.OK:
            return Ret(ret.error)
        select_sections = ret.body

        select_section_list = []
        for select_section in select_sections:
            if select_section.section.course == o_course and select_section.section.term == term and select_section.section.category == category:
                select_section_list.append(select_section)
        return Ret(Error.OK, select_section_list)

    # get o_selectsection by user and section
    @staticmethod
    def get_select_section(o_user, o_section):
        try:
            o_select_section = SelectSection.objects.get(
                user=o_user, section=o_section
            )
        except SelectSection.DoesNotExist:
            return Ret(Error.USER_SECTION_NOT_MATCH)
        return Ret(Error.OK, body=o_select_section)

    @staticmethod
    def select_section(o_user, o_section, bgcolor, color):
        ret = SelectSection.get_select_section(o_user, o_section)
        if ret.error is Error.OK:
            return Ret(Error.SECTION_ALREADY_SELECTED)

        ret = SelectSection.create(o_user, o_section, bgcolor, color)
        if ret.error is not Error.OK:
            return Ret(ret.error)
        return Ret(Error.OK, body=ret.body)

    def to_dict(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            section=self.section.to_dict(),
            bgcolor=self.bgcolor,
            color=self.color,
        )


class Meeting(models.Model):
    L = {
        'day': 12,
        'start': 32,
        'end': 32,
        'room': 32,
        'meeting_dates': 32,
    }

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE
    )

    day = models.CharField(
        max_length=L['day']
    )
    start = models.CharField(
        max_length=L['start']
    )
    end = models.CharField(
        max_length=L['end']
    )
    room = models.CharField(
        max_length=L['room']
    )
    meeting_dates = models.CharField(
        max_length=L['meeting_dates']
    )

    def __str__(self):
        return str(self.section.course.course_code) + ' - ' + str(self.section.section_code)

    # get all meetings for a section
    @staticmethod
    def get_meetings_by_section(o_section):
        meetings = Meeting.objects.filter(section=o_section)
        return Ret(Error.OK, body=meetings)

    @staticmethod
    def delete_meetings_by_section(o_section):
        ret = Meeting.get_meetings_by_section(o_section)
        if ret.error is not Error.OK:
            return Ret(ret.error)
        meetings = ret.body
        for meeting in meetings:
            meeting.delete()
        return Ret(Error.OK)

    def to_dict(self):
        return dict(
            id=self.id,
            day=self.day,
            start=self.start,
            end=self.end,
            room=self.room,
            meeting_dates=self.meeting_dates,
        )
