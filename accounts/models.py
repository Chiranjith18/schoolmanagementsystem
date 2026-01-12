from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')

    def __str__(self):
        return f"{self.user.username} - Teacher"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    attendance = models.PositiveIntegerField(default=0)  # e.g., number of days attended
    #marks = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.user.username} - Student"
    
    

