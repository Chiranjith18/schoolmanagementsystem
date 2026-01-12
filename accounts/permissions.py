from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        # Allow if role=ADMIN OR is_superuser
        return bool(user and user.is_authenticated and (user.role == 'ADMIN' or user.is_superuser))

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'TEACHER'

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'STUDENT'
