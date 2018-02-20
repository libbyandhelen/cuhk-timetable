from django.contrib import admin

from Course.models import Course, Assessment, Component

admin.site.register(Course)
admin.site.register(Component)
admin.site.register(Assessment)
