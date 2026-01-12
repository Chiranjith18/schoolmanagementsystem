from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TeacherProfile, StudentProfile

# ✅ FIXED #1: Custom UserAdmin for ROLE field
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )

# ✅ FIXED #2: Register ALL models properly
admin.site.register(User, CustomUserAdmin)
admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
