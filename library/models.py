from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta


class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.PositiveIntegerField()
    category = models.CharField(max_length=50)
    publication_date = models.DateField(max_length=8)

    def __str__(self):
        return str(self.name) + " ["+str(self.isbn)+']'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    year = models.CharField(max_length=10)                             
    course = models.CharField(max_length=10)                           
    student_no = models.CharField(max_length=3, blank=True) 
    phone = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to="", blank=True)

    def __str__(self):
        return str(self.user) + " ["+str(self.course)+']' + " ["+str(self.year)+']' + " ["+str(self.student_no)+']'


def expiry():
    return datetime.today() + timedelta(days=14)
class IssuedBook(models.Model):
    student_id = models.IntegerField(primary_key=True) 
    isbn = models.CharField(max_length=13)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)
    def __str__(self):
        return self.student_id


class Request(models.Model):
    request = models.CharField(max_length=100, null=True, blank=True)
    


    def __str__(self):
        return self.request
