from django.shortcuts import render
from beneficiary.models import beneficiary_register,userappointments,userbmi
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import datetime 
from django.contrib.auth.decorators import login_required
from datetime import timedelta  
from .decorators import unauthenticated_user,allowed_users
from beneficiary .forms import *
from django.db import connections
from django import forms
from . models import worker_register
from .forms import UserForm,hw_info
from datetime import timedelta
from twilio.rest import Client
from django.contrib.auth import authenticate, login, logout
from django.utils.dateparse import parse_date
from googletrans import Translator
# Create your views here

def registerPage(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        Create_user = hw_info(data=request.POST)
        if user_form.is_valid() and Create_user.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            cruser = Create_user.save(commit=False)
            cruser.user = user
            
            cruser.save()
            registered = True
            return HttpResponseRedirect(reverse('loginPage'))
        else:
            print(user_form.errors,Create_user.errors)
    else:
        user_form = UserForm()
        Create_user = hw_info()
    return render(request,'reg1.html',
                          {'user_form':user_form,
                           'Create_user':Create_user,
                           'registered':registered})

def regBen(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        Create_user = beneficiary_info(data=request.POST)
        if user_form.is_valid() and Create_user.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            cruser = Create_user.save(commit=False)
            cruser.u_user = user
            
            cruser.save()
            registered = True
            return HttpResponseRedirect(reverse('userbmi'))
        else:
            print(user_form.errors,Create_user.errors)
    else:
        user_form = UserForm()
        Create_user = beneficiary_info()
    return render(request,'beneficiary_register.html',
                          {'user_form':user_form,
                           'Create_user':Create_user,
                           'registered':registered})

@unauthenticated_user
def loginPage(request):
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
              

                login(request,user)
                cursor = connections['default'].cursor()
                cursor.execute("SELECT hw_pincode,hw_fname,hw_sname,hw_phno FROM Accounts_worker_register WHERE hw_phno = %s", [username])
                row = cursor.fetchone()
                form1=str(row[0])
                form2=str(row[1])
                form3=str(row[2])
                form4=str(row[3])
               
                request.session['hw_pincode'] = form1
                request.session['hw_fname'] = form2
                request.session['hw_sname'] = form3
                request.session['hw_phno'] = form4
                



                return HttpResponseRedirect(reverse('workerDash'))
        else:
                return HttpResponse("Your account was inactive.")
        
    else:
        return render(request, 'login1.html')

def homePage(request):
    return render(request,"home1.html")

def index(request):

    return render(request,"index.html")
@login_required(login_url='loginPage')  

def workerProfile(request):

    user1 = worker_register.objects.get(hw_phno = request.user)
    context = {'user1':user1}
    return render(request,"user.html",context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers'])   
def workerDash(request):
    form = userappointments.objects.all()
    hwno = request.session.get('hw_pincode')
    ver = form.filter(apdate=date.today(),apPincode = hwno).order_by('apdate')
    
    context = {'form':form,'ver':ver}
    return render(request,"dashboard.html",context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers'])    
def workerPlist(request):
    form = beneficiary_register.objects.all()
    

    ver = form.filter(u_status=True)
    notver = form.filter(u_status=False)
    context = {'form':form,'ver':ver,'notver':notver}
    return render(request,"tables.html",context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers'])    
def workerAppt(request):
    form = userappointments.objects.all()
    
    hwno = request.session.get('hw_pincode')
    ver = form.filter(apdate=date.today(),apPincode = hwno ).order_by('apdate')
   
    datez=date.today()+timedelta(days=1)
    date1= datez+ timedelta(days=14)

    notver = userappointments.objects.filter(apdate__range=(datez, date1),apPincode = hwno ).order_by('apdate')

    #notver = form1.filter(apdate=date.month())
    context = {'form':form,'ver':ver,'notver':notver}
    return render(request,"appointments.html",context)
   
@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers'])    
def timelinepatient(request):

   return render(request,"timelinepatient.html")


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers']) 
def timelineprocess(request):
    id=int(request.POST["id"])
    form = userappointments.objects.all()
    ver = form.filter(u_user_id=id).order_by('apdate')
    form1 = userbmi.objects.all()
    ver1 = form1.filter(u_user_id=id).order_by('bmdate')
    form2 = beneficiary_register.objects.get(u_phno=id)
    return render(request,"timelineprocess.html",{'user1':form2,'ver':ver,'verr':ver1})

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers']) 
def apptdetail(request):

   return render(request,"apptdetail.html")

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers'])
def apptprocess(request):
    id=int(request.POST["id"])
    ver = userappointments.objects.get(apref=id)
    f1 = ver.u_user_id
    form2 = beneficiary_register.objects.get(u_phno=f1)
    return render(request,"apptprocess.html",{'user1':form2,'ver':ver})



def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('loginPage'))


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers'])  
def manualappt(request):
    return render(request,'manualappt.html')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers'])  
def gentimeline1(request):
    id=str(request.POST["userid"])
    datez=request.POST["date"]
    pincode=int(request.POST["pincode"])
    assign=int(request.POST["assigned"])
    atype=int(request.POST["type"])
    phone=str(request.POST["phone"])
    if atype==1:
        aptype=True
    if atype== 0:
        aptype=False
    apstatus = False
    currentdate =parse_date(datez)
    print(currentdate)
    
   
    c1= currentdate - timedelta(days=7)
    c2= currentdate + timedelta(days=7)
    print('################')
    print(c1)
    print(c2)
    a=datez.replace('-', '')+str(id)

    if aptype==False:
        cursor = connections['default'].cursor()
        cursor.execute("SELECT apdate FROM beneficiary_userappointments WHERE aptype=%s AND u_user_id = %s AND apdate BETWEEN %s AND %s", [aptype,id,c1,c2])
        row = cursor.fetchone()
        if row:
            ver = userappointments.objects.filter(apdate__range=(c1, c2),aptype = aptype ,u_user_id = id)
            return render(request,"nonutrition.html",{'ver':ver})
        else:
            cursor.execute("INSERT INTO beneficiary_userappointments(u_user_id,apdate,apref,apassign,apPincode,aptype,apstatus,apPhone) VALUES( %s , %s ,%s,%s,%s,%s,%s,%s)", [id, datez,a,assign,pincode,aptype,apstatus,phone])
            return HttpResponseRedirect(reverse('workerDash'))

    else:
        cursor = connections['default'].cursor()
        cursor.execute("INSERT INTO beneficiary_userappointments(u_user_id,apdate,apref,apassign,apPincode,aptype,apstatus,apPhone) VALUES( %s , %s ,%s,%s,%s,%s,%s,%s)", [id, datez,a,assign,pincode,aptype,apstatus,phone])
        return HttpResponseRedirect(reverse('workerDash'))
   
def absent(request):
    
    form = userappointments.objects.all()
    
    hwno = request.session.get('hw_pincode')
    ver = form.filter(apdate=date.today(),apPincode = hwno ).order_by('apdate')
   
    datez=date.today()-timedelta(days=1)
    date1= date.today()- timedelta(days=7)

    notver = userappointments.objects.filter(apdate__range=(date1,datez),apPincode = hwno,apstatus=False ).order_by('apdate')

    #notver = form1.filter(apdate=date.month())
    context = {'form':form,'notver':notver}
    return render(request,"absent.html",context)



def localsms(request):
    translator = Translator(service_urls=[
      'translate.google.com',
      
    ])

    lang = request.POST['lang']
     
    hwfname = str(request.session.get('hw_fname'))
    hwsname = str(request.session.get('hw_sname'))
    hwphone = str(request.session.get('hw_phno'))


    form = userappointments.objects.all()
    hwno = request.session.get('hw_pincode')
    tommorow = date.today()+timedelta(days=1)
    ver = form.filter(apdate=tommorow,apPincode=hwno,apstatus=False)
    account_sid = 'AC3239aa7e879998bb1ebb7be3a1a497fe'
    auth_token = '8d16a2cade7b63322f9b8710c7f68db4'
    client = Client(account_sid, auth_token)
    
    for i in ver:
        msg = "Hey " +i.u_user_id+" Please attend you appointment with id: "+ i.apref+" for the date: "+ str(i.apdate)+" Registered at: "+ str(i.apPhone)+" For any Query Contact: "+hwfname+"  "+hwsname+ " at "+hwphone
        a  = translator.translate(msg,dest=lang)
        print(a.text)
        
        message = client.messages \
                        .create(
                            body = a.text,
                            from_='+12058529824',
                            to="+91"+i.apPhone
                        )
                    

        print(message.sid)
    
    return HttpResponseRedirect(reverse('workerDash'))





def localsms1(request):
        translator = Translator(service_urls=[
       'translate.google.com',
      
        ])
        lang = request.POST['lang']
        hwfname = str(request.session.get('hw_fname'))
        hwsname = str(request.session.get('hw_sname'))
        hwphone = str(request.session.get('hw_phno'))
        form = userappointments.objects.all()
        hwno = request.session.get('hw_pincode')
        tommorow = date.today()
        ver = form.filter(apdate=tommorow,apPincode=hwno,apstatus=False)
        account_sid = 'AC3239aa7e879998bb1ebb7be3a1a497fe'
        auth_token = '8d16a2cade7b63322f9b8710c7f68db4'
        client = Client(account_sid, auth_token)
        
        for i in ver:
            msg = "Hey " +i.u_user_id+" You missed your appointment with id: "+ i.apref+" for the date: "+ str(i.apdate)+" Registered at: "+ str(i.apPhone)+" For any Query Contact: "+hwfname+"  "+hwsname+ " at "+hwphone
            a  = translator.translate(msg,dest=lang)
           

            

            message = client.messages \
                            .create(
                                body=a.text,
                                from_='+12058529824',
                                to="+91"+i.apPhone
                            )

            print(message.sid)
        return HttpResponseRedirect(reverse('workerDash'))
