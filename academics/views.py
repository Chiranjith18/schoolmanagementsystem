from datetime import datetime
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.permissions import IsAdmin, IsStudent, IsTeacher
from django.contrib.auth import logout, authenticate, login  
from django.shortcuts import render, redirect 
from accounts.models import StudentProfile, TeacherProfile, User  # ✅ FIXED: Added User import
from .models import *
from .serializers import *
from drf_spectacular.utils import extend_schema
from django.contrib.auth.decorators import login_required

# ✅ FIXED #1: PROPER BulkCreateMixin that handles ForeignKeys
class BulkCreateMixin:
    """✅ FIXED: Now handles ForeignKey IDs → actual objects"""
    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):  # Bulk from Swagger
            objects = []
            for item in data:
                # ✅ FIXED: Convert ID → actual model instances
                validated = self.get_serializer(data=item)
                validated.is_valid(raise_exception=True)
                
                # Handle ForeignKeys by looking up actual objects
                instance_data = {}
                for field, value in validated.validated_data.items():
                    field_obj = self.serializer_class.Meta.model._meta.get_field(field)
                    if field_obj.is_relation:  # ForeignKey
                        instance_data[field] = field_obj.related_model.objects.get(id=value)
                    else:
                        instance_data[field] = value
                
                obj = self.serializer_class.Meta.model(**instance_data)
                objects.append(obj)
            
            self.queryset.model.objects.bulk_create(objects)
            return Response({"success": f"Created {len(objects)} items"}, 
                          status=status.HTTP_201_CREATED)
        return super().create(request, *args, **kwargs)

# ✅ FIXED #2: ViewSets now work with proper ForeignKey handling
@extend_schema(tags=["Admin/semesters"])
class SemesterViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

@extend_schema(tags=["Admin/subjects"])
class SubjectViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

@extend_schema(tags=["Admin/assessments"])
class AssessmentTypeViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    queryset = AssessmentType.objects.all()
    serializer_class = AssessmentTypeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

@extend_schema(tags=["Admin/assignments"])
class TeacherAssignmentViewSet(BulkCreateMixin, viewsets.ModelViewSet):
    queryset = TeacherAssignment.objects.all()
    serializer_class = TeacherAssignmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

# ✅ FIXED #3: AssignMarksView - Proper ID handling
@extend_schema(tags=["Teacher/marks"])
class AssignMarksView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsTeacher]

    @extend_schema(
    request=AssignMarksSerializer,
    responses={200: dict}
    )
    def post(self, request):
        teacher = request.user
        assignment_id = request.data.get("assignment")

        # 🔐 SECURITY CHECK - Convert ID to object
        try:
            assignment = TeacherAssignment.objects.get(id=assignment_id, teacher=teacher)
        except TeacherAssignment.DoesNotExist:
            return Response({"error": "You are not assigned to this subject"}, 
                          status=status.HTTP_403_FORBIDDEN)

        serializer = AssignMarksSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 🔁 UPSERT with proper ForeignKey handling
        student = StudentProfile.objects.get(id=serializer.validated_data['student'].id)
        assessment = AssessmentType.objects.get(id=serializer.validated_data['assessment'].id)

        obj, created = StudentMarks.objects.update_or_create(
            student=student,
            assignment=assignment,
            assessment=assessment,
            defaults={'marks': serializer.validated_data['marks']}
        )

        return Response({"success": "Marks saved", "created": created}, status=status.HTTP_200_OK)

# ✅ REST OF VIEWS (UNCHANGED - WORKING FINE)

@extend_schema(tags=["Students"])
class MyMarksView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent]

    def get(self, request):
        student_profile = request.user.student_profile
        marks_qs = StudentMarks.objects.filter(student=student_profile).select_related(
            'assignment__subject', 'assignment__semester', 'assessment')

        result = {}
        for m in marks_qs:
            sem_key = str(m.assignment.semester)
            subject_name = m.assignment.subject.name
            assessment_name = m.assessment.name

            result.setdefault(sem_key, {})
            result[sem_key].setdefault(subject_name, {})
            result[sem_key][subject_name][assessment_name] = m.marks

        return Response(result)

@extend_schema(tags=["Students"])
class MyAttendanceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent]

    def get(self, request):
        student = request.user.student_profile
        attendance_qs = StudentAttendance.objects.filter(student=student).select_related(
            'assignment__subject', 'assignment__semester')

        result = {}
        for att in attendance_qs:
            sem_key = str(att.assignment.semester)
            subject_name = att.assignment.subject.name

            result.setdefault(sem_key, {})
            if subject_name not in result[sem_key]:
                result[sem_key][subject_name] = {'present': 0, 'total': 0}

            result[sem_key][subject_name]['total'] += 1
            if att.present:
                result[sem_key][subject_name]['present'] += 1

        for sem in result:
            for subject in result[sem]:
                data = result[sem][subject]
                data['percentage'] = round((data['present'] / data['total']) * 100, 2) if data['total'] else 0

        return Response(result)

# Teacher ViewSets (minor security fixes)
@extend_schema(tags=["Teacher/marks"])
class TeacherMarksViewSet(viewsets.ModelViewSet):
    serializer_class = AssignMarksSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsTeacher]

    def get_queryset(self):
        return StudentMarks.objects.filter(assignment__teacher=self.request.user)

    def perform_create(self, serializer):
        assignment = serializer.validated_data['assignment']
        if assignment.teacher != self.request.user:
            raise PermissionError("Not assigned to this subject")
        serializer.save()

@extend_schema(tags=["Teacher/attendance"])
class TeacherAttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsTeacher]

    def get_queryset(self):
        return StudentAttendance.objects.filter(assignment__teacher=self.request.user)

    def perform_create(self, serializer):
        assignment = serializer.validated_data['assignment']
        if assignment.teacher != self.request.user:
            raise PermissionError("Not allowed")
        serializer.save()

# ✅ FIXED #4: Template Views (already good, minor optimizations)
@login_required
def student_dashboard_template(request):
    if not hasattr(request.user, 'student_profile'):
        return redirect('home')
    
    student = request.user.student_profile
    marks_qs = StudentMarks.objects.filter(student=student).select_related(
        'assignment__subject', 'assignment__semester', 'assessment')
    attendance_qs = StudentAttendance.objects.filter(student=student).select_related(
        'assignment__subject', 'assignment__semester')

    marks, attendance = {}, {}
    # Marks processing...
    for m in marks_qs:
        sem_key = str(m.assignment.semester)
        marks.setdefault(sem_key, {}).setdefault(m.assignment.subject.name, {})[m.assessment.name] = m.marks

    # Attendance processing...
    for att in attendance_qs:
        sem_key = str(att.assignment.semester)
        subject_name = att.assignment.subject.name
        attendance.setdefault(sem_key, {}).setdefault(subject_name, {'present': 0, 'total': 0})
        attendance[sem_key][subject_name]['total'] += 1
        if att.present:
            attendance[sem_key][subject_name]['present'] += 1

    for sem in attendance:
        for subject in attendance[sem]:
            data = attendance[sem][subject]
            data['percentage'] = round((data['present'] / data['total']) * 100, 2) if data['total'] else 0

    return render(request, "student_dashboard.html", {"marks": marks, "attendance": attendance})

@login_required
def teacher_dashboard_template(request):
    if not hasattr(request.user, 'teacher_profile'):
        return redirect('home')
    
    students = StudentProfile.objects.all().select_related('user')
    assignments = TeacherAssignment.objects.filter(teacher=request.user).select_related('subject', 'semester')
    assessments = AssessmentType.objects.all()
    marks = StudentMarks.objects.filter(assignment__teacher=request.user).select_related(
        'student__user', 'assignment__subject', 'assessment')
    attendance = StudentAttendance.objects.filter(assignment__teacher=request.user).select_related(
        'student__user', 'assignment__subject',
    )
    
    if request.method == "POST" and "date" in request.POST:  # Attendance form submitted
        student_id = request.POST.get("student")
        assignment_id = request.POST.get("assignment")
        date_str = request.POST.get("date")
        present = request.POST.get("present") == 'on'

        student = StudentProfile.objects.get(id=student_id)
        assignment = TeacherAssignment.objects.get(id=assignment_id)
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        StudentAttendance.objects.update_or_create(
            student=student,
            assignment=assignment,
            date=date_obj,
            defaults={"present": present}
        )

        return redirect('teacher-dashboard')
    
     # ✅ HANDLE MARKS FORM SUBMISSION
    if request.method == "POST" and "marks" in request.POST:  # Marks form submitted
        student_id = request.POST.get("student")
        assignment_id = request.POST.get("assignment")
        assessment_id = request.POST.get("assessment")
        marks_value = request.POST.get("marks")

        # Convert to proper types
        student = StudentProfile.objects.get(id=student_id)
        assignment = TeacherAssignment.objects.get(id=assignment_id, teacher=request.user)  # security check
        assessment = AssessmentType.objects.get(id=assessment_id)

        # ✅ ADD/UPDATE MARKS
        StudentMarks.objects.update_or_create(
            student=student,
            assignment=assignment,
            assessment=assessment,
            defaults={'marks': int(marks_value)}
        )

        return redirect('teacher-dashboard')  # Redirect to avoid resubmission
    
    return render(request, "teacher_dashboard.html", {
        "students": students, "assignments": assignments,
        "assessments": assessments, "marks": marks,
         "attendance": attendance,
    })
  

@login_required
def admin_dashboard_template(request):
    if request.user.role != 'ADMIN':
        return redirect('home')
    
    teachers = TeacherProfile.objects.select_related('user')
    students = StudentProfile.objects.select_related('user')
    
    return render(request, "admin_dashboard.html", {"teachers": teachers, "students": students})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

# ✅ FIXED #5: Login view (already fixed in your code)
def html_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == "STUDENT":
                return redirect('student-dashboard')
            elif user.role == "TEACHER":
                return redirect('teacher-dashboard')
            elif user.role == "ADMIN":
                return redirect('admin-dashboard')
        return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")
