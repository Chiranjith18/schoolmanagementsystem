from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    MyAttendanceView,
    MyMarksView,
    SemesterViewSet,
    SubjectViewSet,
    AssessmentTypeViewSet,
    TeacherAssignmentViewSet,
    TeacherAttendanceViewSet,
    TeacherMarksViewSet,
    AssignMarksView,
    student_dashboard_template, 
    teacher_dashboard_template,  
    admin_dashboard_template,   
    logout_view,                 
    html_login_view,             
)

# ✅ FIXED: Proper router setup - ALL registrations FIRST
router = DefaultRouter()
router.register(r'admin/semesters', SemesterViewSet)
router.register(r'admin/subjects', SubjectViewSet)
router.register(r'admin/assessments', AssessmentTypeViewSet)
router.register(r'admin/assignments', TeacherAssignmentViewSet)
router.register(r'teacher/marks', TeacherMarksViewSet, basename='teacher-marks')
router.register(r'teacher/attendance', TeacherAttendanceViewSet, basename='teacher-attendance')

urlpatterns = router.urls 

# ✅ FIXED: Template views with proper names
urlpatterns += [
    path('teacher/assign-marks/', AssignMarksView.as_view(), name='assign-marks'),
    path('student/my-marks/', MyMarksView.as_view(), name='my-marks'),
    path('student/my-attendance/', MyAttendanceView.as_view(), name='my-attendance'),
    path('login/', html_login_view, name='academics-login'),          
    path('logout/', logout_view, name='logout'),             
    
    # Dashboard URLs
    path('dashboard/student/', student_dashboard_template, name='student-dashboard'),
    path('dashboard/teacher/', teacher_dashboard_template, name='teacher-dashboard'),
    path('dashboard/admin/', admin_dashboard_template, name='admin-dashboard'),
]
