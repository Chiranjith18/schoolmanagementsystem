from django.shortcuts import redirect, render


# schoolmanagement/views.py
def home(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'student_profile'):
            return redirect('student-dashboard')
        elif hasattr(request.user, 'teacher_profile'):
            return redirect('teacher-dashboard')
        elif request.user.role == 'ADMIN':
            return redirect('admin-dashboard')
    return render(request, "login.html")
