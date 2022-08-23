
from library.forms import IssueBookForm
from django.shortcuts import redirect, render,HttpResponse
#HttpResponse: provides an inbound HTTP request to a Django web application with a text response
# Redirect: Returns an HttpResponseRedirect to the appropriate URL for the arguments passed
# render: used to load a template and a context, it is like a short cut to HttpResponse which provides a more effective way to modify templates, and load data dynamically as compared to HttpResponse
from .models import *
from .forms import IssueBookForm
from django.contrib.auth import authenticate, login, logout
# authentication verifies a user is who they claim to be
from . import forms, models
from datetime import date
from django.contrib.auth.decorators import login_required
# login_required:  secures views in your web applications by forcing the client to authenticate with a valid logged-in User
import math
from django.contrib import messages
#messages: used to display flash messages or notifications to both authenticated and anonymous users
from .forms import IssueBookForm

from django.contrib.auth.mixins import LoginRequiredMixin
#LoginRequiredMixin: Verifies that the current user is authenticated.
from django.views.generic import ListView

from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import ChatForm


from django.utils import timezone
from django.urls import reverse_lazy
 
 #ListView: A page representing a list of objects. While this view is executing, self. object_list will contain the list of objects
 #NB: A QuerySet is a collection of data from a database
#

def index(request):
    return render(request, "index.html")    #render: Return an HttpResponse whose content is filled with the result of calling django.template.loader.render_to_string() with the passed arguments.


# Found In the drop down menu of books 'Add a book' option


@login_required(login_url = '/admin_login')
def add_book(request):
    if request.method == "POST":
# the result of request.method =="POST" is a boolean value - TRUE if the current request from a user was performed using the HTTP "POST" method
# It submits data to be processed (e.g from an HTML form) to the identified resource.The data is included in the body of the request. 
# This may result in creation of a new resource
# or the updates of existing resources or both.

# In this case it will bring a form with the given records below and the librarian must input the data of the book accordingly so that it is 
# added to the database 
        name = request.POST['name']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category = request.POST['category']
        publication_date = request.POST['publication date']


        books = Book.objects.create(name=name, author=author, isbn=isbn, category=category , publication_date=publication_date)
        books.save()
        # the above two lines, 
        #this performs an update SQL statement behind the scenes, n only after calling save() will django hit the database

        alert = True
        

        return render(request, "add_book.html", {'alert':alert})
        # when the book has been added to the database, we defined a variable 'alert' which should show that book addition was successful
        # and this alert ("Book is added successfully") message will be found in the "add_book.html"


    return render(request, "add_book.html")



# Read

#Found In the drop down menu of books 'view all books' option of the admin


@login_required(login_url = '/admin_login')
def view_books(request):   
    books = Book.objects.all() 
    return render(request, "view_books.html", {'books':books}) 
# the above code works the same as explained in the next code below


# Found in the "available books" option of the student
 
@login_required(login_url = '/student_login')
def student_view_books(request):  # this is where the student will be able to see the books in the library
    books = Book.objects.all()
    #the above line returns a copy of the current QuerySet(or QuerySet subclass)
    # After calling all() on an object, you'll have a QuerySet to work with
    return render(request, "student_view_books.html", {'books':books}) 
    #the above line causes displays of all the books available in the database and directs one to the template "student_view_books.html"





# Found in the "All Students" option of the admin
# The below code works the same as the one above

@login_required(login_url = '/admin_login')
def view_students(request):
    students = Student.objects.all()
    return render(request, "view_students.html", {'students':students})



# Found in the request option on the "issue button" of the admin 

@login_required(login_url = '/admin_login')
def issue_book(request):
    form = IssueBookForm()       # As created in the 'forms.py', this form gets both the information about the book requested and the student who requests for it
    if request.method == "POST":
        form = IssueBookForm(request.POST)
        if form.is_valid():           # Returns True if the form has no errors oand False otherwise.
            obj = models.IssuedBook()
            obj.student_id = request.POST['name2']
            obj.isbn = request.POST['isbn2']
            obj.save()                            #Here this performs an update SQL statement behind the scenes, n only after calling save() will django hit the database 
            
            return redirect('/adminrequest')      # after the issue, we should be redirected back to the request page of the admin
           
    return render(request, "issue_book.html", {'form':form})
    

@login_required(login_url = '/admin_login')
def view_issued_book(request):
    issuedBooks = IssuedBook.objects.all() # this variable is attached to all the information about all issued books getting them from the model:  IssuedBook(column of issued books in the database), refer to models.py to see the class IssuedBook
    details = [] # the details are made in form of a list
    # 
    for i in issuedBooks:  # for any item in issuedbook QuerySet, the below codes should apply, i stands for item
        issdate=str(i.issued_date.day)+'/'+str(i.issued_date.month)+'/'+str(i.issued_date.year)
        expdate=str(i.expiry_date.day)+'/'+str(i.expiry_date.month)+'/'+str(i.expiry_date.year)
        # The above two lines show how the issue and expiry dates will be displayed in the 'view_issued_book.html',page of all issued books
        days = (date.today()-i.issued_date)
        # the above calculation finds the number of days a student has stayed with the book
        d=days.days
        fine=0
        if d>16: # if the number of days stayed with the book exceed 16
            day=d-17
            rate=10000/7 # rate of fine since we want the fine to be UGX 15000 after 10 days 
            fine=math.ceil(5000+((day)*rate)) # we add a UGX 5000 because by the 17 days, it will be 3 days past the expiry date (book is supposed to be had for 14 days ) and since day=number of days - 17, that will be 17-17=0, therefore:(5000+((day)*rate)) will be (5000+(0)*10000/7)= UGX 5000 so on the 18th day, the rate starts adding 
            
        books = list(models.Book.objects.filter(isbn=i.isbn))  # this is a list containing all the books, .filter() filters a search, and allows to return only rows that match the search term in this case it is 'i.isbn' that means an item in isbn column

        students = list(models.Student.objects.filter(user=i.student_id)) # this is a list containing all the students, .filter() filters a search, and allows to return only rows that match the search term in this case it is 'i.student_id' that means an item in the student_id column
        i=0   # at 1st, there are no issued books so we make the items in the issuedBooks be 0
        for b in books:    # for any item in book QuerySet, the below codes should apply, b stands for item (we created a for loop)
            
            t=(students[i].user,students[i].user_id,books[i].name,books[i].isbn,issdate,expdate,d,fine)  # we are making a turple (It stores multiple items in a single variable, in this case, it is storing it in t) with borrower's username, borrower library id, book name, isbn, the book's issue n expiry dates and the fine
            i=i+1   # when a turple t is added, the items in the issuedBooks are added by one
            details.append(t)  # from above, we defined a variable: details which is a list, here we are adding our made turple to the end of the list
    return render(request, "view_issued_book.html", {'issuedBooks':issuedBooks, 'details':details})



#.filter() filters a search, and allows to return only rows that match the search term 

@login_required(login_url = '/student_login')
def student_issued_books(request):
    student = Student.objects.filter(user_id=request.user.id) # this will filter to get the information of the specific student
    issuedBooks = IssuedBook.objects.filter(student_id=student[0].user_id)  # this will filter to get the book information of the book issued to the above filtered student if they have any
    li1 = []     # we are defining a list that will contain turples with book information
    li2 = []     # we are defining a list that will contain turples with date information and fine

    for i in issuedBooks:
        books = Book.objects.filter(isbn=i.isbn)   # the book will be filter through the rest in the database using its ISBN since all books have unique ISBNs
        for book in books:
            t=(request.user.id, request.user.get_full_name, book.name,book.author)
            li1.append(t)   # adding a turple at the end of the list li1
# the fine is as explained in the above code
        days=(date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>16:
            day=d-17
            rate=10000/7  
            fine=math.ceil(5000+((day)*rate)) 
            
        t=(issuedBooks[0].issued_date, issuedBooks[0].expiry_date,d, fine)  # t is a turple to contain issued n expiry dates and the fine
        li2.append(t)      # adding a turple at the end of the list li2
    return render(request,'student_issued_books.html',{'li1':li1, 'li2':li2})

@login_required(login_url = '/student_login')
def profile(request):
    return render(request, "profile.html")  # this displays the student's profile as defined in the profile.html

@login_required(login_url = '/student_login')
def edit_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        course = request.POST['course']
        year = request.POST['year']
        student_no = request.POST['student_no']

        student.user.email = email
        student.phone = phone
        student.course = course
        student.year = year
        student.student_no = student_no
        student.user.save()
        student.save()
        alert = True
        return render(request, "edit_profile.html", {'alert':alert})
    return render(request, "edit_profile.html")

def delete_book(request, myid):
    books = Book.objects.filter  (id=myid)
    books.delete()
    return redirect("/view_books")

def delete_student(request, myid):
    students = Student.objects.filter(id=myid)
    students.delete()
    return redirect("/view_students")



def delete_issue(request,pk):
    book= IssuedBook.objects.get(student_id=pk) 
    book.delete()
    return redirect('/view_issued_book')
    



 




def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "change_password.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "change_password.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "change_password.html")



# Sign Up 


def student_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        course = request.POST['course']
        year = request.POST['year']
        student_no = request.POST['student_no']
        image = request.FILES['image']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            passnotmatch = True
            return render(request, "student_registration.html", {'passnotmatch':passnotmatch})

        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        student = Student.objects.create(user=user, phone=phone, course=course, year=year,student_no=student_no, image=image)
        user.save()
        student.save()
        alert = True
        return render(request, "student_registration.html", {'alert':alert})
    return render(request, "student_registration.html")





# Authentication


def student_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a student!!")
            else:
                return redirect("/profile")
        else:
            alert = True
            return render(request, "student_login.html", {'alert':alert})
    return render(request, "student_login.html")

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/add_book")
            else:
                return HttpResponse("You are not an admin.")
        else:
            alert = True
            return render(request, "admin_login.html", {'alert':alert})
    return render(request, "admin_login.html")

def Logout(request):
    logout(request)
    return redirect ("/")





















#Request


@login_required
def request(request):
	if request.method == 'POST':
		requested_book= request.POST['request']
		current_user = request.user
		student_id = current_user.id
		username = current_user.username
		user_request = username + "   [" + requested_book.upper() +"]" 

		a = Request(request=user_request)
		a.save()
		messages.success(request, 'Request was sent')
		return render(request,"request.html")
	else:
	    messages.error(request, '')
	    return render(request,"request.html")






class ViewRequest(LoginRequiredMixin,ListView):
	model = Request
	template_name = 'admin_request.html'
	context_object_name = 'requests'
	paginate_by = 10000000

	def get_queryset(self):
		return Request.objects.order_by('-id')



def delete_request(request,myid):
    request= Request.objects.filter(id=myid) 
    request.delete()
    return redirect('/adminrequest')





















# Admin
class ACreateChat(LoginRequiredMixin, CreateView):
	form_class = ChatForm
	model = Chat
	template_name = 'adminchatform.html'
	success_url = reverse_lazy('alchat')


	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)




class AListChat(LoginRequiredMixin, ListView):
	model = Chat
	template_name = 'adminchatlist.html'

	def get_queryset(self):
		return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')






# student

class UCreateChat(LoginRequiredMixin, CreateView):
	form_class = ChatForm
	model = Chat
	template_name = 'studentchatform.html'
	success_url = reverse_lazy('ulchat')


	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)


class UListChat(LoginRequiredMixin, ListView):
	model = Chat
	template_name = 'studentchatlist.html'

	def get_queryset(self):
		return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')






def delete_chat(request,myid):
    x= Chat.objects.filter(id=myid) 
    x.delete()
    return redirect('/alchat')
















