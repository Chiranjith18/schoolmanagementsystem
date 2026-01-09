import email
from django.shortcuts import render



from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Teacher

class teacherAPI(APIView):
    def post(self, request):
        print(request.data)
        
        new_tea = Teacher(
            name=request.data['name'],
            subject=request.data['subject'],
            age=request.data.get('age', 10),
            email=request.data.get('email') or None
        )
        new_tea.save()
        return Response({"message": "Teacher created successfully", "id": new_tea.id})
        
    def get(self, request, teacher_id=None):  
        if teacher_id is not None:
            # Get single teacher by ID from URL
            teacher = Teacher.objects.get(id=teacher_id)
            return Response({
                "id": teacher.id,
                "name": teacher.name,
                "subject": teacher.subject,
                "age": teacher.age,
                "email": teacher.email
            })
        
       
        all_teachers = Teacher.objects.all()
        teachers_list = []
        for teacher in all_teachers:
            teachers_list.append({
                "id": teacher.id,
                "name": teacher.name,
                "subject": teacher.subject,
                "age": teacher.age,
                "email": teacher.email
            })
        return Response(teachers_list)
    
    def patch(self, request, teacher_id):  
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.name = request.data.get('name', teacher.name)
        teacher.subject = request.data.get('subject', teacher.subject)
        teacher.age = request.data.get('age', teacher.age)
        teacher.email = request.data.get('email', teacher.email)
        teacher.save()
        return Response({"message": "Teacher updated successfully"})
    
    def delete(self, request, teacher_id):  
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.delete()
        return Response({"message": "Teacher deleted successfully"})