# from django.shortcuts import render


# def home(request):
#     return render(request, "home.html")


# def profile(request):
#     return render(request, "profile.html")


# def dashboard(request):
#     student = {
#         "name": "chiranjith",
#         "age": 19,
#         "gender": "male",
#     }
#     marks = 50
#     subjects = ["maths", "science", "english", "social"]
#     return render(request, "dashboard.html", {"student": student, "marks": marks, "subjects": subjects})




from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student

class studentAPI(APIView):
    def post(self,request):
        print(request.data)

        new_std=Student(name=request.data['name'],age=request.data['age'])
        new_std.save()
        return Response("created")
