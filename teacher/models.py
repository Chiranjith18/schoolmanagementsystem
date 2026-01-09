from django.db import models

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    age = models.IntegerField(default=10)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name