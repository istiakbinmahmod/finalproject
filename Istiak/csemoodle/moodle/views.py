from django.shortcuts import render, redirect
import random
import os
import hashlib
import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
# from .models import people
from django.db import connection
from django import template
# Create your views here.
from .loginOrSignUp import loginOrSignup
def home(request):
    return render(request, 'homepage.html')

def profileadmincreatecourses(request):
    try:
        usr = request.session['username']
    except:
        user_logout(request)
    if request.method == 'POST':
        courseid = request.POST.get('courseid')
        sessionid = request.POST.get('sessionid')
        coursetitle = request.POST.get('coursetitle')
        credithour = request.POST.get('credithour')
        sql = "INSERT INTO COURSE(COURSE_ID, SESSION_ID, COURSE_TITLE, CREDIT_HOUR) VALUES(%s, %s, %s, %s)"
        try:
            cur = connection.cursor()
            cur.execute(sql, [courseid, sessionid, coursetitle, credithour])
            connection.commit()
            cur.close()
            return redirect('/home/profile/admin/createcourses')
        except:
            return redirect('/home/profile/admin/createcourses/')
    name = request.session['username']
    return render(request, 'create_courses.html', {'name': name})

def profileadminassignstucourses(request):

    try:
        usr = request.session['username']
    except:
        user_logout(request)
    if request.method == 'POST':
        profileid = request.POST.get('profileid')
        courseid = request.POST.get('courseid')
        sessionid = request.POST.get('sessionid')
        sql = "INSERT INTO STUDENTCOURSERELATION(PROFILE_ID, COURSE_ID, SESSION_ID) VALUES(%s, %s, %s)"
        try:
            cur = connection.cursor()
            cur.execute(sql, [profileid, courseid, sessionid])
            connection.commit()
            cur.close()
            return redirect('/home/profile/admin/assignstucourses')
        except:
            return redirect('/home/profile/admin/assignstucourses/')
    name = request.session['username']
    return render(request, 'assign_students_to_course.html', {'name': name})

def profileadminassignteacourses(request):
    try:
        usr = request.session['username']
    except:
        user_logout(request)
    if request.method == 'POST':
        profileid = request.POST.get('profileid')
        courseid = request.POST.get('courseid')
        sessionid = request.POST.get('sessionid')
        sql = "INSERT INTO INSTRUCTORCOURSERELATION(PROFILE_ID, COURSE_ID, SESSION_ID) VALUES(%s, %s, %s)"
        try:
            cur = connection.cursor()
            cur.execute(sql, [profileid, courseid, sessionid])
            print(profileid)
            print(courseid)
            print(sessionid)
            connection.commit()
            cur.close()
            return redirect('/home/profile/admin/assignteacourses')
        except:
            return redirect('/home/profile/admin/assignteacourses/')
    name = request.session['username']
    return render(request, 'assign_teachers_to_course.html', {'name': name})
