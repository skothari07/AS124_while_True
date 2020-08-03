from django.urls import path,include
from . import views
urlpatterns = [
    path("loginBen/",views.loginBen,name="loginBen"),
    path("registerBen/",views.registerBen,name="registerBen"),
    path("homeBen/",views.homeBen,name="homeBen"),
    path("logout", views.logout_request, name="logout"),
    path('userbmi',views.index,name='userbmi'),
    path('display',views.displaybmi,name='displaybmi'),
    path('timelinegen',views.timelinegen,name="timelinegen"),
    path('gentimeline',views.gentimeline,name='gentimeline'),
    path('checktimeline',views.checktimeline,name='checktimeline'),
    path('timelinepage',views.timelinepage,name='timelinepage'),
    path('visitapptid',views.visitapptid,name='visitapptid'), 
    path('userbmiapptid',views.userbmiapptid,name='userbmiapptid'),
    path('displayappt',views.displayappt,name='displayappt'),
    path('rescheduleRef',views.rescheduleRef,name='rescheduleRef'),
    path('rescheduleDetail',views.rescheduleDetail,name='rescheduleDetail'),
    path('rescheduleprocess',views.rescheduleprocess,name='rescheduleprocess'),
    path('beneficiaryappt',views.beneficiaryappt,name='beneficiaryappt'),
    path('beneficiaryhealth',views.beneficiaryhealth,name='beneficiaryhealth'),
    path('verifyRef',views.verifyRef,name='verifyRef'),
    path('verifyDetail',views.verifyDetail,name='verifyDetail'),
    path('verifyprocess',views.verifyprocess,name='verifyprocess'),
    path("logoutpage",views.logoutpage,name="logoutpage"),

]
    
  
    
