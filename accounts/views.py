from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import (
    UserSerializer,
    TeacherProfileSerializer,
    StudentProfileSerializer,
    LoginSerializer
)
from .models import User, TeacherProfile, StudentProfile
from .permissions import IsAdmin
from drf_spectacular.utils import extend_schema



# -------------------
# LOGIN
# -------------------
@extend_schema(tags=["Auth"])
class LoginView(APIView):
    authentication_classes = []   # Anyone can login
    permission_classes = []

    @extend_schema(
    request=LoginSerializer,
    responses={
        200: UserSerializer,
        401: dict,
    },
    auth=[]
    )

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data
        })



# -------------------
# CREATE TEACHER
# -------------------
@extend_schema(tags=["Admin"])
class CreateTeacherView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @extend_schema(
    request=TeacherProfileSerializer,
    responses={201: dict, 400: dict},
   )

    def post(self, request):
        data = request.data
        
        if isinstance(data, list):  # Bulk create
            results = []
            for item in data:
                result = self.create_single_teacher(item)
                results.append(result)
            return Response({"results": results}, status=status.HTTP_201_CREATED)
        else:  # Single create
            result = self.create_single_teacher(data)
            return Response(result['data'], status=result['status'])  # ✅ FIXED: Return dict with status

    def create_single_teacher(self, data):
        """✅ FIXED: Returns dict {data, status} instead of tuple"""
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        

        if User.objects.filter(username=username).exists():
            return {
                'data': {"error": f"Username {username} exists"}, 
                'status': status.HTTP_400_BAD_REQUEST
            }

        # ✅ FIXED: Create user + profile in transaction
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password, 
            role='TEACHER'
        )
        TeacherProfile.objects.create(user=user)

        return {
            'data': {"success": f"Teacher {username} created"}, 
            'status': status.HTTP_201_CREATED
        }

@extend_schema(tags=["Admin"])
class CreateStudentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @extend_schema(
    request=StudentProfileSerializer,
    responses={201: dict, 400: dict},
)

    def post(self, request):
        """✅ FIXED: Proper Response handling for SINGLE + BULK"""
        data = request.data
        
        if isinstance(data, list):  # Bulk
            results = []
            for item in data:
                result = self.create_single_student(item)
                results.append(result['data'])
            return Response({"results": results}, status=status.HTTP_201_CREATED)
        else:  # Single
            result = self.create_single_student(data)
            return Response(result['data'], status=result['status'])  # ✅ FIXED

    def create_single_student(self, data):
        """Returns dict {data, status}"""
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
      

        if User.objects.filter(username=username).exists():
            return {
                'data': {"error": f"Username '{username}' already exists"}, 
                'status': status.HTTP_400_BAD_REQUEST
            }

        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password, 
            role='STUDENT'
        )
        StudentProfile.objects.create(user=user)

        return {
            'data': {"success": f"Student '{username}' created successfully"}, 
            'status': status.HTTP_201_CREATED
        }



# -------------------
# LIST TEACHERS
# -------------------
@extend_schema(tags=["Admin"])
class ListTeachersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @extend_schema(
    responses={200: TeacherProfileSerializer(many=True)},
   )

    def get(self, request):
        teachers = TeacherProfile.objects.all()
        serializer = TeacherProfileSerializer(teachers, many=True)
        return Response(serializer.data)


# -------------------
# LIST STUDENTS
# -------------------
@extend_schema(tags=["Admin"])
class ListStudentsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @extend_schema(
    responses={200: StudentProfileSerializer(many=True)},
    )

    def get(self, request):
        students = StudentProfile.objects.all()
        serializer = StudentProfileSerializer(students, many=True)
        return Response(serializer.data)


# -------------------
# DELETE TEACHER BY ID
# -------------------
@extend_schema(tags=["Admin"])
class DeleteTeacherView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @extend_schema(
    responses={
        200: dict,
        404: dict,
    }
   )

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id, role='TEACHER')
            user.delete()
            return Response({"success": "Teacher deleted"})
        except User.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)


# -------------------
# DELETE ALL TEACHERS
# -------------------
@extend_schema(tags=["Admin"])
class DeleteAllTeachersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @extend_schema(
    responses={200: dict}
   )

    def delete(self, request):
        users = User.objects.filter(role='TEACHER')
        count = users.count()
        users.delete()
        return Response({"success": f"{count} teachers deleted"})


# -------------------
# DELETE STUDENT BY ID
# -------------------
@extend_schema(tags=["Admin"])
class DeleteStudentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @extend_schema(
    responses={
        200: dict,
        404: dict,
    }
)

    def delete(self, request, id):
        
        try:
           user = User.objects.get(id=id, role='STUDENT')  # ✅ FIXED: Get User by ID and role
           user.delete()
           return Response({"success": "Student deleted"})
        except User.DoesNotExist:
           return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)


# -------------------
# DELETE ALL STUDENTS
# -------------------
@extend_schema(tags=["Admin"])
class DeleteAllStudentsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    @extend_schema(
    responses={200: dict}
   )

    def delete(self, request):
        users = User.objects.filter(role='STUDENT')
        count = users.count()
        users.delete()
        return Response({"success": f"{count} students deleted"})
