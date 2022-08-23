from django.urls import path
from . import views


urlpatterns = [
    # format: path("the link to the website",views.the view with related information,name="the name that you give to the view in case you need to refer to it")



    
    path("", views.index, name="index"),
    path("logout/", views.Logout, name="logout"),

    #admin

    path("add_book/", views.add_book, name="add_book"),
    path("view_books/", views.view_books, name="view_books"),
    path("view_students/", views.view_students, name="view_students"),
    path("issue_book/", views.issue_book, name="issue_book"),
    path("view_issued_book/", views.view_issued_book, name="view_issued_book"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("delete_book/<int:myid>/", views.delete_book, name="delete_book"),
    path("delete_student/<int:myid>/", views.delete_student, name="delete_student"),
    path("delete_issue/<int:pk>/", views.delete_issue, name="delete_issue"),
    path('adminrequest/', views.ViewRequest.as_view(), name='adminrequest'),
    path("delete_request/<int:myid>/", views.delete_request, name="delete_request"),
    path('acchat/', views.ACreateChat.as_view(), name='acchat'),
    path('alchat/', views.AListChat.as_view(), name='alchat'),
    path("delete_chat/<int:myid>/", views.delete_chat, name="delete_chat"),


    #student


    path("student_view_books/", views.student_view_books, name="student_view_books"),
    path("student_issued_books/", views.student_issued_books, name="student_issued_books"),
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("student_registration/", views.student_registration, name="student_registration"),
    path("change_password/", views.change_password, name="change_password"),
    path("student_login/", views.student_login, name="student_login"),
    path('request/', views.request, name='request'),
    path('ucchat/', views.UCreateChat.as_view(), name='ucchat'),
    path('ulchat/', views.UListChat.as_view(), name='ulchat'),













]