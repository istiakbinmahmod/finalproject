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


def user_login(request):
    print("i m log in")
    try:
        usr = request.session['username']
        user_logout(request)
        #return redirect('/homepage')
    except:
        print("not logged in please log in")
    if request.method == 'POST':
        # email = request.POST.get('email')
        # print(email)
        profileid = request.POST.get('profileid')
        password = request.POST.get('password')
        print(password)
        msg = 'Enjoy Buying!'
        try:
            cur = connection.cursor()
            sql = "select profile_id, KEY ,SALT, name, email_id, phone_no, date_of_birth, profile_picture, city, street, is_student, is_teacher from PEOPLE where profile_id = %s"
            print(sql)
            print(profileid)
            cur.execute(sql,[profileid])
            result = cur.fetchone()
            dic_res = []
            # dbemail = None
            dbprofileid = None
            dbkey = None
            dbsalt = None
            dbname = None
            dbemail = None
            dbphoneno = None
            dbdob = None
            dbpropic = None
            dbcity = None
            dbstreet = None
            dbisstu = None
            dbistea = None
            dbuserid = result[0]
            dbkey = result[1]
            dbsalt = result[2]
            dbname = result[3]
            dbemail = result[4]
            dbphoneno = result[5]
            dbdob = str(result[6])
            dbpropic = result[7]
            dbcity = result[8]
            dbstreet = result[9]
            dbisstu = result[10]
            dbistea = result[11]
            """
            img = 'uploads/products/10000069-2_28-fresho-capsicum-green.jpg'
            try:
                img = request[5]
            except:
                print('failed to load image!')
            request.session['img_url']=img
            """
            print("from database:...")
            print("dbuserid:" + dbuserid)
            if dbuserid == profileid:
                print("username verified")
                new_key =hashlib.pbkdf2_hmac(
                    'sha256',  # The hash digest algorithm for HMAC
                    password.encode('utf-8'),
                    dbsalt ,
                    100000, # 100,000 iterations of SHA-256
                    # dklen = 128
                )

                if new_key == dbkey:
                    print("success")
                    print("sql:" + sql)
                    # request.session.__setitem__('username',dbuser)
                    request.session['userprofileid'] = dbuserid
                    request.session['username'] = dbname
                    request.session['useremail'] = dbemail
                    request.session['userphoneno'] = dbphoneno
                    request.session['userdob'] = dbdob
                    request.session['userpropic'] = dbpropic
                    request.session['usercity'] = dbcity
                    request.session['userstreet'] = dbstreet
                    request.session['userisstu'] = dbisstu
                    request.session['useristea'] = dbistea
                    """dbemail = None
                    dbphoneno = None
                    dbdob = None
                    dbpropic = None
                    dbcity = None
                    dbstreet = None"""

                    # request.session.__setitem__('username',username)
                    print("success2")
                    print("username from session: " + request.session['username'])
                    if dbisstu == 1:
                        return redirect('/home/profile/student')
                    elif dbistea == 1:
                        return redirect('/home/profile/teacher')
                    else:
                        return redirect('/home/profile/admin')
                    # return redirect('/home')
                else:
                    print("failed man!")
                    print("dbkey: ")
                    print(dbkey)
                    print("userkey: ")
                    print(new_key)
                    return redirect('/home/profilelogin')

            else:
                print("wrong username!")
                return redirect('/home/profilelogin')
        except:
            messages = "something went wrong! try again"
            print(messages)
            return render(request,'login.html',{'msg':messages})
    else:
        return render(request, 'login.html', {})

"""
def test(request):
    return render(request,'hello.html',{})


def lol(request):
    return render(request, 'lol.html', {})
"""

def user_signup(request):
    print("i m in signup")
    usr=None
    try:
        usr = request.session['username']
        user_logout(request)
    except:
        print("sign up please!")
        print("couldn't make it")
    if request.method == 'POST':
        profileid = request.POST.get('profileid')
        #id = random.randrange(start=1700000, step=1)
        #print("id:" + str(id))
        name = request.POST.get('name')
        #print(usrname)
        #username = request.POST.get('username')
        #print(username)
        password = request.POST.get('password')
        emailid = request.POST.get('mail')
        phoneno = request.POST.get('phonono')
        #gender = request.POST.get('gender')
        dob = request.POST.get('birthdate')
        propic = request.POST.get('propic')
        img = request.FILES['propic']
        img_extension = os.path.splitext(img.name)[1]
        user_folder = 'static/profilepic/'
        if not os.path.exists(user_folder):
            os.mkdir(user_folder)
        # uploading image
        img_save_path = user_folder + 'propic' + str(profileid) + img_extension
        # img_save_path = user_folder + 'pro_pic'+img_extension
        img_url = 'profilepic/' + 'propic' + str(profileid) + img_extension
        print(img_url)
        #request.session['propic'] = img_url
        #print(request.session['img_url'])
        with open(img_save_path, 'wb') as f:
            for chunk in img.chunks():
                print('writing in folder and database')
                f.write(chunk)
        profilepic = img_url
        city = request.POST.get('city')
        street = request.POST.get('street')
        role = request.POST.get('role')
        #zone = request.POST.get('zone')
        #method = request.POST.get('paymentmethod')
        salt = os.urandom(32)
        # password = 'password123'
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000,  # 100,000 iterations of SHA-256
            # dklen=128  #128 byte key
        )

        sql = "INSERT INTO PEOPLE(profile_id, KEY ,SALT, name, email_id, phone_no, date_of_birth, profile_picture, city, street, is_student, is_teacher) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = connection.cursor()
            if role == 'student':
                cursor.execute(sql, [profileid, key, salt, name, emailid, phoneno, dob, profilepic, city, street, 1, 0])
            elif role == 'teacher':
                cursor.execute(sql, [profileid, key, salt, name, emailid, phoneno, dob, profilepic, city, street, 0, 1])
            else:
                cursor.execute(sql, [profileid, key, salt, name, emailid, phoneno, dob, profilepic, city, street, 0, 0])
            connection.commit()
            cursor.close()
            return redirect('/homepage')
        except:
            return render(request,'signup.html',{'message':'Something went wrong!'})
    else:
        return render(request, 'signup.html', {})



def user_logout(request):
    try:
            # del request.session['username']
            # del request.session['name']
            #request.session.delete('username')
            #request.session.delete('userprofileid')
            request.session.flush()
            print("logged out")
            # user = request.session['username']
            return redirect('/homepage')

            # if user is None:
            #     print("log out success")

    except:
        print("something is wrong")
        return render(request, 'logout.html')

def profilestudenthome(request):
    try:
        usr = request.session['username']
    except:
        user_logout(request)
    name = request.session['username']
    profileid = request.session['userprofileid']
    print(profileid)
    print(name)
    cur = connection.cursor()
    sql = "select course_id, session_id from studentcourserelation where profile_id = %s"
    cur.execute(sql, [profileid])
    results = cur.fetchall()
    dict_result = []
    for r in results:
        cour_id = r[0]
        sess_id = r[1]
        """
        sql2 = "select course_id, session_id, course_title, credit_hour from course where sess_id = %s"
        cur.execute(sql, [sess_id])
        resultss = cur.fetchall()
        """
        row = {'cou_id':r[0], 'ses_id':r[1]}
        dict_result.append(row)
    cur.close()
    connection.commit()
    return render(request, 'homepagestudent.html', {'courses':dict_result})
def profileteacherhome(request):
    try:
        usr = request.session['username']
    except:
        user_logout(request)
    name = request.session['username']
    return render(request, 'homepageteacher.html', {'name':name})
def profileadminhome(request):
    try:
        usr = request.session['username']
    except:
        user_logout(request)
    """
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
            return redirect('/home/profile/admin')
        except:
            return redirect('/home/profile/admin')
    """
    name = request.session['username']
    return render(request, 'homepageadmin.html', {'name':name})

