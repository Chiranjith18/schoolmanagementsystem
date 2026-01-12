from django.contrib import admin
from .models import *

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['year', 'semester']

@admin.register(Subject) 
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

@admin.register(AssessmentType)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'max_marks']

admin.site.register([TeacherAssignment, StudentMarks, StudentAttendance])
