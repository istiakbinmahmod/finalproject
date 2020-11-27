from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from . import views
#from .checkout import checkout
from .loginOrSignUp import loginOrSignup
#from .Sales import sale

app_name = 'loginorsignup'

urlpatterns = [
    path('',views.home, name = 'homepage'),
    path('homepage/', views.home),
    path('home/profile/student/', loginOrSignup.profilestudenthome, name = 'profilestudentpage'),
    path('home/profile/teacher/', loginOrSignup.profileteacherhome, name = 'profileteacherpage'),
    path('home/profile/admin/', loginOrSignup.profileadminhome, name = 'profileadminpage'),
    path('home/profile/admin/createcourses/', views.profileadmincreatecourses, name = 'profileadminpagecreatecourses'),
    path('home/profile/admin/assignstucourses/', views.profileadminassignstucourses, name = 'profileadminpageassignstucourses'),
    path('home/profile/admin/assignteacourses/', views.profileadminassignteacourses, name = 'profileadminpageassignteacourses'),
    path('home/profilelogin/', loginOrSignup.user_login, name='user_login'),
    path('home/homepage/signup/', loginOrSignup.user_signup, name = 'user_signup'),
    path('home/homepage/logout/', loginOrSignup.user_logout, name = 'user_logout'),
    path('home/profile/student/course/', loginOrSignup.student_to_course, name='course_inside')
]
