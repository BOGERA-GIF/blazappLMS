from django import forms
from django.contrib.auth.models import User
from . import models





#form to handle issuing of books to students which will ask for the book name and ISBN and also ask for the student's name,course year and student no


class IssueBookForm(forms.Form):
    isbn2 = forms.ModelChoiceField(queryset=models.Book.objects.all(), empty_label="Book Name [ISBN]", to_field_name="isbn", label="Book Details")
    name2 = forms.ModelChoiceField(queryset=models.Student.objects.all(), empty_label="Name [Course] [Year] [Student No]", to_field_name="user", label="Student Details")
    
    isbn2.widget.attrs.update({'class': 'form-control'})
    name2.widget.attrs.update({'class':'form-control'})


    #ModelChoiceField - A ChoiceField whose choices are a model QuerySet.
    #ModelChoiceField will give the librarian ability to look through all the available books by tracking their ISBN and also the usernames of all available students 
    #This enables the librarian to choose the book requested and issue it to the student that has requested for it accordingly
    #empty_label - Words that will appear in the two fields before the librarian clicks on the field
    #to_field_name - this will take them to the field with the information related to the desired field i.e user has student details while isbn has the book details
    #queryset=models.Book.objects.all() - will get all the information requireed of the available books in the database
    #queryset=models.Student.objects.all() - will get all the information required of the available students in the database

