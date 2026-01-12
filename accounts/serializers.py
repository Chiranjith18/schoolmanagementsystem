from rest_framework import serializers
from .models import User
from .models import User, TeacherProfile, StudentProfile



    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role']


class TeacherProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = TeacherProfile
        fields = ['id', 'username', 'email']

class StudentProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = StudentProfile
        fields = ['id', 'username', 'email']
        
        