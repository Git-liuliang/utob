# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render,HttpResponse
import smtplib
from email.mime.text import MIMEText
import random,pymysql,json,time
from cmdb.models import userinfo
# Create your views here.

def homepage(request):
    return render(request,'index.html')

def registry(request):
    if request.method == "POST":



            print(request.POST.get('username'))
            print(request.POST.get('email'))
            print(request.POST.get('password'))
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            conn = pymysql.connect(host="172.18.3.189", user="root", passwd="xinwei", db="utob")
            cur = conn.cursor()
            sql = "insert cmdb_userinfo(email,username,password,createtime) VALUES('%s','%s','%s',now())"%(email,username,password)
            mous = cur.execute(sql)
            conn.commit()

            return HttpResponse(json.dumps({"status": 1, "result": "注册失败"}))




def sendEmail(to_email):

    random_code = makecode(6)
    _user = "894513081@qq.com"
    _pwd = "gzpsdvdyzgusbchi"
    _to = to_email
    msg = MIMEText("your code is %s"%random_code)
    msg["Subject"] = "NEW Bee CMDB"
    msg["From"] = _user
    msg["To"] = _to

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
        print("Success!")
    except  smtplib.SMTPException as e:
        print("Falied,%s" % e)
    return random_code

def makecode(num):
    '''用户输入验证码位数，随机生成带有字母和数字的验证码'''
    res = ''
    for i in range(num):
        zimu = chr(random.randint(97,122))
        digt = str(random.randint(0,9))
        res += random.choice([zimu,digt])
    return res

#write cache to redis
def write_to_cache(email,random_code):

    print('sssssssssssss')
    cache.set("code_"+email,{"email":email,"random_code":random_code})
    print("aaaaaaa")


##select cache to redis

def select_to_cache(email):
    ss = cache.get(email)
    if ss == None:
        cache.set(email,0)
        cache.expire(email, 86400)
        res = 0
        return res
    else:
        res = cache.get(email)+1
        cache.set(email,res)
        cache.expire(email, 86400)
        return res

#write info to mysql

# def check_email(to_email):
#
#     conn = pymysql.connect(host="172.18.3.189", user="root", passwd="xinwei", db="utob")
#     cur = conn.cursor()
#     sql = "select id from cmdb_userinfo where email= '%s'"%to_email
#     res = cur.execute(sql)
#     conn.commit()
#     return res

def check(request):
    if request.method == "POST":
        res = request.POST
        column = list(res.keys())[0]
        to_something = list(res.values())[0]
        conn = pymysql.connect(host="172.18.3.189", user="root", passwd="xinwei", db="utob")
        cur = conn.cursor()
        sql = "select id from cmdb_userinfo where %s= '%s'"%(column,to_something)
        mous = cur.execute(sql)
        conn.commit()
        if not mous:
            if  cache.get(to_something) is None or cache.get(to_something) < 3 :
                # random_code = sendEmail(to_something)
                select_to_cache(to_something)
                write_to_cache(to_something,'123456')
                status = 0
                result = ""
                return HttpResponse(json.dumps({"status": status, "result": result}))
            else:
                status = 1
                result = "注册次数超过3次"
                return HttpResponse(json.dumps({"status": status, "result": result}))
        else:
            status = 1
            result = 'email已使用'
            return HttpResponse(json.dumps({"status": status, "result": result}))


def validate_name(request):
    if request.method == "POST":
        res = request.POST
        column = list(res.keys())[0]
        to_something = list(res.values())[0]
        conn = pymysql.connect(host="172.18.3.189", user="root", passwd="xinwei", db="utob")
        cur = conn.cursor()
        sql = "select id from cmdb_userinfo where %s= '%s'"%(column,to_something)
        mous = cur.execute(sql)
        conn.commit()
        if not mous:
                status = 0
                result = ""
                return HttpResponse(json.dumps({"status": status, "result": result}))
        else:
            status = 1
            result = 'username已使用'
            return HttpResponse(json.dumps({"status": status, "result": result}))


def validate_code(request):
    js_email = request.POST.get("email")
    js_code = request.POST.get("code")
    print(js_email)
    print(js_code)
    key = cache.get("code_"+js_email)
    print(key)
    if js_email and key:

        back_code = key.get("random_code")
        if back_code == js_code:
            return HttpResponse(json.dumps({"status": 0, "result": "ok"}))
        else:
            return HttpResponse(json.dumps({"status": 1, "result": "验证码错误"}))

    else:
        return HttpResponse(json.dumps({"status": 1, "result": "email无效"}))