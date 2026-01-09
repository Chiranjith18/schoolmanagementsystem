from django.db import models

# class SampleTable(models.Model):
#     age = models.IntegerField(default=10)
#     weight = models.FloatField(null=True)
#     name = models.CharField(max_length=150)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     date_of_birth = models.DateField(auto_now=True)
#     date_of_birth_with_time = models.DateTimeField()
#     birth_time = models.TimeField()
#     is_admin = models.BooleanField()


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()


