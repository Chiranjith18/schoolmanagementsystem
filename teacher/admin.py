from django.contrib import admin

from .models import Teacher

class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "email")
    search_fields = ("name", "subject", "email")
    list_filter=("subject",)
admin.site.register(Teacher, TeacherAdmin)