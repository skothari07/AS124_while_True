from django.shortcuts import render,redirect
from . forms import beneficiary_info,UserForm,usr
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from . models import *
from datetime import datetime  
from datetime import timedelta  
from twilio.rest import Client
from twilio.rest import Client
from django.contrib.auth.decorators import login_required
from django.db import connections
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user,allowed_users
# Create your views here.
@unauthenticated_user
def loginBen(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                cursor = connections['default'].cursor()
                cursor.execute("SELECT u_user_id FROM beneficiary_userappointments WHERE u_user_id = %s", [username])
                row = cursor.fetchone()
                form1=str(row[0])
               
                request.session['u_user_id'] = form1
                return HttpResponseRedirect(reverse('homeBen'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
           
         return render(request,"beneficiary_login.html")

def registerBen(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        Create_user = beneficiary_info(data=request.POST)
        if user_form.is_valid() and Create_user.is_valid():
            user = user_form.save(commit=False)
            cruser = Create_user.save(commit=False)

            cruser.u_user = user
            cruser.u_verified = request.user
            random_number = User.objects.make_random_password(length=6, allowed_chars='123456789')
            cruser.u_phno = random_number
            user.username = cruser.u_phno
            
            user.set_password(user.password)
            msgFname = cruser.u_fname
            msgSname = cruser.u_sname
            msgUid  = random_number
            msgWid = cruser.u_verified
            msgDate = str(date.today())
            msgPhone = cruser.u_phone
            hwfname = request.session.get('hw_fname')
            hwsname = request.session.get('hw_sname')
            hwphone = request.session.get('hw_phno')
            user.save()
            cruser.save()
            
            account_sid = 'AC3239aa7e879998bb1ebb7be3a1a497fe'
            auth_token = '8d16a2cade7b63322f9b8710c7f68db4'
            client = Client(account_sid, auth_token)
           


            message = client.messages \
                                .create(
                                    body="Hello " +msgFname+" "+msgSname+" Your id is "+msgUid+" registered at: "+msgPhone+" By " +hwfname+" "+hwsname+ " "+hwphone+" on Date "+msgDate,
                                    from_='+12058529824',
                                    to="+91"+msgPhone
                                )

            print(message.sid)
            state = cruser.u_states
            
            request.session['u_phno'] = cruser.u_phno
            request.session['u_phone'] = cruser.u_phone
            cursor1 = connections['default'].cursor()

            cursor1.execute("UPDATE beneficiary_states SET s_count = s_count+1 WHERE s_states = %s", [state])
            request.session['u_phno'] = cruser.u_phno
            request.session['u_phone'] = cruser.u_phone

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


@login_required(login_url='loginBen')  
def homeBen(request):
    phno = request.session.get('u_user_id')
    print(phno)
    user1 = beneficiary_register.objects.get(u_phno = request.user)
    user2 = userappointments.objects.filter(u_user_id=phno)
    context = {'user1':user1,'user2':user2}
    
    return render(request,"beneficiary_home.html",context)


def logout_request(request):
    logout(request)
    return HttpResponseRedirect(reverse('loginBen'))
@login_required(login_url='loginPage')

def index(request):
    #if request.method=="GET":  
    form1 = request.session.get('u_phno')
    forms = usr()
    return render(request,'form.html',{'form':forms,'form1':form1})

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers']) 
def displaybmi(request):
    w=float(request.POST["bmweight"])
    h=float(request.POST["bmheight"])
    z=h/100
    z1=w
    bb=z1/((z)**2)
    bmi = round(bb, 2)
    bid=request.session.get('u_phno')
    date=(request.POST["bmdate"])
    blood=float(request.POST["bmblood"])
    bmworker = request.user

    cursor = connections['default'].cursor()
    cursor.execute("INSERT INTO beneficiary_userbmi(u_user_id,bmdate,bmworker,currentbmi,bmweight,bmheight,bmblood) VALUES( %s , %s,%s , %s, %s ,%s , %s )", [bid, date,bmworker,bmi,w,h,blood])
    userdisp={'id':bid,'date':date,bmworker:'bmworker','currentbmi':bmi,'weight':w,'height':h,'blood':blood}
    return render(request,"result.html",{'vals':userdisp})

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers']) 
def timelinegen(request):
      id= request.session.get('u_phno')
      return render(request,'timelinegen.html',{'id':id})
    
@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers'])  
def gentimeline(request):
    id=str(request.POST["userid"])
    request.session['u_phno'] = id
    
    z = str(request.session.get('hw_pincode'))
    ph = str(request.session.get('u_phone'))
    v = str(request.user)
    date1=datetime.now()+ timedelta(days=30)
    date2=datetime.now()+ timedelta(days=60)
    date3=datetime.now()+ timedelta(days=90)
    x1=1
    x2=2
    x3=3
    aptype=True
    a = datetime.date(date1).strftime("%Y%m%d")
    b = datetime.date(date2).strftime("%Y%m%d")
    c = datetime.date(date3).strftime("%Y%m%d")
    a = a+str(id)
    b = b+str(id)
    c = c+str(id)
    cursor = connections['default'].cursor()
    apstatus = False
    cursor.execute("INSERT INTO beneficiary_userappointments(u_user_id,apdate,apno,apref,apassign,apPincode,aptype,apstatus,apPhone) VALUES( %s , %s ,%s,%s,%s,%s,%s,%s,%s)", [id, date1,x1,a,v,z,aptype,apstatus,ph])
    cursor.execute("INSERT INTO beneficiary_userappointments(u_user_id,apdate,apno,apref,apassign,apPincode,aptype,apstatus,apPhone) VALUES( %s , %s ,%s,%s,%s,%s,%s,%s,%s)", [id, date2,x2,b,v,z,aptype,apstatus,ph])
    cursor.execute("INSERT INTO beneficiary_userappointments(u_user_id,apdate,apno,apref,apassign,apPincode,aptype,apstatus,apPhone) VALUES( %s , %s ,%s,%s,%s,%s,%s,%s,%s)", [id, date3,x3,c,v,z,aptype,apstatus,ph])

    return HttpResponseRedirect(reverse('timelinepage'))

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers'])  
def checktimeline(request):
  return render(request,'checktimeline.html')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers']) 
def timelinepage(request):
    id=request.session.get('u_phno')
    
    vals= userappointments.objects.filter(u_user_id=id)
    return render(request,'timelinepage.html',{'rows':vals})
    
@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers']) 

def visitapptid(request):
    
    return render(request,'visitapptid.html')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers']) 
def userbmiapptid(request):
    refid=str(request.POST["userid"])
    val=True
    val1 = str(request.user)
    cursor = connections['default'].cursor()

    cursor.execute("SELECT u_user_id,apstatus FROM beneficiary_userappointments WHERE apref = %s", [refid])
    row = cursor.fetchone()
    form1=str(row[0])
    form2 = row[1]
    print(form2)
    if form2 == 0:
        cursor1 = connections['default'].cursor()
        cursor1.execute("UPDATE beneficiary_userappointments SET apstatus = %s WHERE apref = %s", [val,refid])
        cursor1.execute("UPDATE beneficiary_userappointments SET apreceived = %s WHERE apref = %s", [val1,refid])
        cursor = connections['default'].cursor()
        cursor.execute("SELECT u_user_id,apstatus FROM beneficiary_userappointments WHERE apref = %s", [refid])

   
   
    forms = usr()
    return render(request,'visitapptbmi.html',{'form':forms,'useridpass':form1,'form2':form2})


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers']) 
def displayappt(request):
    w=float(request.POST["bmweight"])
    h=float(request.POST["bmheight"])
    z=h/100
    z1=w
    bb=z1/((z)**2)
    bmi = round(bb, 2)
    bid=request.session.get('u_phno')
    date=(request.POST["bmdate"])
    blood=float(request.POST["bmblood"])
    bmworker = request.user

    cursor = connections['default'].cursor()
    cursor.execute("INSERT INTO beneficiary_userbmi(u_user_id,bmdate,bmworker,currentbmi,bmweight,bmheight,bmblood) VALUES( %s , %s,%s , %s, %s ,%s , %s )", [bid, date,bmworker,bmi,w,h,blood])
    userdisp={'id':bid,'date':date,bmworker:'bmworker','currentbmi':bmi,'weight':w,'height':h,'blood':blood}
    return render(request,"resultappt.html",{'vals':userdisp})


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers']) 
def rescheduleRef(request):

            
    
    return render(request,'rescheduleRef.html')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers']) 
def rescheduleDetail(request):
    refid=str(request.POST["userid"])
    val1 = str(request.user)
    cursor1 = connections['default'].cursor()
    cursor1.execute("UPDATE beneficiary_userappointments SET apreceived = %s WHERE apref = %s", [val1,refid])
    cursor = connections['default'].cursor()
    s = 0
    cursor.execute("SELECT u_user_id,apdate,apstatus FROM beneficiary_userappointments WHERE apref = %s", [refid])    
    row = cursor.fetchone()
    form1=str(row[0])
    form2 = row[1]
    form2 = str(form2)
    form3 =row[2]
    print(form3)
    return render(request,'rescheduleDetail.html',{'useridpass':form1,'form2':form2,'refid':refid,'form3':form3})

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers']) 
def rescheduleprocess(request):
    refid=str(request.POST["refid"])
    newdate= str(request.POST["newdate"])
    cursor1 = connections['default'].cursor()
    cursor1.execute("UPDATE beneficiary_userappointments SET apdate = %s WHERE apref = %s", [newdate,refid])
    return render(request,'dashboard.html')


@login_required(login_url='loginBen')
def beneficiaryhealth(request):
    phno = request.session.get('u_user_id')
    user2 = userbmi.objects.all()
    verr = user2.filter(u_user_id=phno).order_by('bmdate')
    
    context = {'verr':verr}
    
    return render(request,'beneficiaryhealth.html',context)

@login_required(login_url='loginBen')
def beneficiaryappt(request):
    phno = request.session.get('u_user_id')
    user2 = userappointments.objects.all()
    ven = user2.filter(u_user_id=phno).order_by('apdate')
    ver=ven.filter(apstatus=True)
    notver=ven.filter(apstatus=False)
   

    context = {'ver':ver,'notver':notver}
    return render(request,'beneficiary_appts.html',context)


def logoutpage(request):
    logout(request)
    return HttpResponseRedirect(reverse('loginBen'))












@allowed_users(allowed_roles=['healthworkers']) 
def verifyRef(request):
     return render(request,'verifyRef.html')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers']) 
def verifyDetail(request):
    userid =str(request.POST["userid"])
    val1 = beneficiary_register.objects.get(u_phno=userid)
    
    cursor = connections['default'].cursor()
    cursor.execute("SELECT u_fname FROM beneficiary_beneficiary_register WHERE u_phno = %s", [userid])
   
    row = cursor.fetchone()
    form1=str(row[0])
    form2 = row[0]
    form2 = str(form2)
   
    return render(request,'verifyDetail.html',{'useridpass':form1,'form2':form2,'refid':userid})

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['healthworkers']) 
def verifyprocess(request):
    userid=str(request.POST["userid"])
    status= str(request.POST["status"])
    cursor1 = connections['default'].cursor()
    cursor1.execute("UPDATE beneficiary_beneficiary_register SET u_status = %s WHERE u_phno = %s", [status,userid])
    return render(request,'dashboard.html')


