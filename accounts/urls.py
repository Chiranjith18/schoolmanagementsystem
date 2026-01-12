from django.urls import path
from .views import (
    LoginView,
    CreateTeacherView, CreateStudentView,
    ListTeachersView, ListStudentsView,
    DeleteTeacherView, DeleteAllTeachersView,
    DeleteStudentView, DeleteAllStudentsView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),

    path('teachers/create/', CreateTeacherView.as_view()),
    path('students/create/', CreateStudentView.as_view()),
    path('teachers/', ListTeachersView.as_view()),
    path('students/', ListStudentsView.as_view()),
     # DELETE
    path('teachers/delete/<int:id>/', DeleteTeacherView.as_view()),
    path('teachers/delete-all/', DeleteAllTeachersView.as_view()),

    path('students/delete/<int:id>/', DeleteStudentView.as_view()),
    path('students/delete-all/', DeleteAllStudentsView.as_view()),
]
