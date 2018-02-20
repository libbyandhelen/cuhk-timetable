from django.db import models

from base.error import Error
from base.response import Ret


class Course(models.Model):
    L = {
        'course_code': 32,
        'course_name': 100,
        'career': 32,
        'grading_basis': 32,
        'add_consent': 32,
        'drop_consent': 32,
        'enroll_requirement': 300,
        'description': 800,

        'learning_outcome': 800,
        'course_syllabus': 800,
        'feedback': 800,
        'required_reading': 800,
        'recommended_reading': 800,
    }
    course_code = models.CharField(
        max_length=L['course_code'],
        unique=True,
    )
    course_name = models.CharField(
        max_length=L['course_name'],
    )
    career = models.CharField(
        max_length=L['career'],
        null=True,
    )
    units = models.FloatField(
        null=True,
    )
    grading_basis = models.CharField(
        max_length=L['grading_basis'],
        null=True,
    )
    add_consent = models.CharField(
        max_length=L['add_consent'],
        null=True,
    )
    drop_consent = models.CharField(
        max_length=L['drop_consent'],
        null=True,
    )
    enroll_requirement = models.CharField(
        max_length=L['enroll_requirement'],
        null=True,
    )
    description = models.CharField(
        max_length=L['description'],
        null=True,
    )

    learning_outcome = models.CharField(
        max_length=L['learning_outcome'],
        null=True,
    )
    course_syllabus = models.CharField(
        max_length=L['course_syllabus'],
        null=True,
    )
    feedback = models.CharField(
        max_length=L['feedback'],
        null=True,
    )
    required_reading = models.CharField(
        max_length=L['required_reading'],
        null=True,
    )
    recommended_reading = models.CharField(
        max_length=L['recommended_reading'],
        null=True,
    )

    def __str__(self):
        return str(self.id)+'  '+self.course_code

    def update_info(self, outcome, syllabus, feedback, required_reading, recommended_reading):
        self.learning_outcome = outcome,
        self.course_syllabus = syllabus,
        self.feedback = feedback,
        self.required_reading = required_reading,
        self.recommended_reading = recommended_reading
        self.save()

    @staticmethod
    def get_course_by_code(code):
        try:
            o_course = Course.objects.get(course_code=code)
        except:
            return Ret(Error.COURSE_NOT_EXIST)
        return Ret(Error.OK, body=o_course)

    def to_dict(self):
        return dict(
            id=self.id,
            course_code=self.course_code,
            course_name=self.course_name,
            career=self.career,
            units=self.units,
            grading_basis=self.grading_basis,
            add_consent=self.add_consent,
            drop_consent=self.drop_consent,
            enroll_requirement=self.enroll_requirement,
            description=self.description,
            learning_outcome=self.learning_outcome,
            course_syllabus=self.course_syllabus,
            feedback=self.feedback,
            required_reading=self.required_reading,
            recommended_reading=self.recommended_reading,
        )

    @staticmethod
    def get_course_by_id(course_id):
        try:
            o_course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Ret(Error.COURSE_NOT_EXIST)
        return Ret(Error.OK, body=o_course)


class Component(models.Model):
    L = {
        'name': 32,
        'note': 32,
    }

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=L['name'],
    )
    note = models.CharField(
        max_length=L['note'],
    )

    def __str__(self):
        return self.course.course_code

    # get all the components of a course
    @staticmethod
    def get_component_by_course(o_course):
        components = Component.objects.filter(course=o_course)
        return Ret(Error.OK, components)

    @staticmethod
    def delete_component_by_course(o_course):
        ret = Component.get_component_by_course(o_course)
        if ret.error is not Error.OK:
            return Ret(ret.error)
        components = ret.body

        for component in components:
            component.delete()
        return Ret(Error.OK)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            note=self.note,
        )


class Assessment(models.Model):
    L = {
        'type': 32,
        'percent': 32,
    }

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )

    type = models.CharField(
        max_length=L['type'],
    )
    percent = models.CharField(
        max_length=L['percent']
    )

    def __str__(self):
        return self.course.course_code

    # get all assessments of a course
    @staticmethod
    def get_assessment_by_course(o_course):
        assessments = Assessment.objects.filter(course=o_course)
        return Ret(Error.OK, assessments)

    @staticmethod
    def delete_assessment_by_course(o_course):
        ret = Assessment.get_assessment_by_course(o_course)
        if ret.error is not Error.OK:
            return Ret(ret.error)
        assessments = ret.body

        for assessment in assessments:
            assessment.delete()
        return Ret(Error.OK)

    def to_dict(self):
        return dict(
            id=self.id,
            type=self.type,
            percent=self.percent,
        )
