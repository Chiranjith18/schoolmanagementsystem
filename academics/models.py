from django.db import models
from accounts.models import User, StudentProfile

class Semester(models.Model):
    year = models.IntegerField()      # 1,2,3,4
    semester = models.IntegerField()  # 1 or 2

    def __str__(self):
        return f"Year {self.year} - Sem {self.semester}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class AssessmentType(models.Model):
    name = models.CharField(max_length=50)  
    # Internal 1, Internal 2, Semester 1, Semester 2
    max_marks = models.IntegerField(default=100)

    def __str__(self):
        return self.name


class TeacherAssignment(models.Model):
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'TEACHER'}
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('teacher', 'subject', 'semester')

    def __str__(self):
        return f"{self.teacher.username} - {self.subject}"


class StudentMarks(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='academic_marks'   # ⚠ FIXED CLASH
    )
    assignment = models.ForeignKey(TeacherAssignment, on_delete=models.CASCADE)
    assessment = models.ForeignKey(AssessmentType, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)

    class Meta:
        unique_together = ('student', 'assignment', 'assessment')

class StudentAttendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    assignment = models.ForeignKey(
        'TeacherAssignment', 
        on_delete=models.CASCADE
    )  # links teacher + subject + semester
    date = models.DateField()
    present = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'assignment', 'date')

    def __str__(self):
        status = "Present" if self.present else "Absent"
        return f"{self.student.user.username} - {self.assignment.subject.name} on {self.date}: {status}"
