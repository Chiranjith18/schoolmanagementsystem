from rest_framework import serializers
from .models import Semester, StudentAttendance, StudentMarks, Subject, AssessmentType, TeacherAssignment

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class AssessmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentType
        fields = '__all__'


class TeacherAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAssignment
        fields = '__all__'

class AssignMarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentMarks
        fields = [
            'student',
            'assignment',
            'assessment',
            'marks'
        ]


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = ['student', 'assignment', 'date', 'present']