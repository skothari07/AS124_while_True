from django.urls import path
from . import views
urlpatterns = [
    path("loginPage",views.loginPage,name="loginPage"),
    path("registerPage",views.registerPage,name="registerPage"),
    path("homepage",views.homePage,name="homePage"),
    path("",views.index,name="index"),
    path("workerDash",views.workerDash,name="workerDash"),
    path("workerProfile",views.workerProfile,name="workerProfile"),
    path("workerPlist",views.workerPlist,name="workerPlist"),
    path("workerAppt",views.workerAppt,name="workerAppt"),
    path("logoutpage",views.logout_page,name="logoutpage"),
    path("timelinepatient",views.timelinepatient,name="timelinepatient"),
    path("timelineprocess",views.timelineprocess,name="timelineprocess"),
    path("apptdetail",views.apptdetail,name="apptdetail"),
    path("apptprocess",views.apptprocess,name="apptprocess"),
    path("manualappt",views.manualappt,name="manualappt"),
    path('gentimeline1',views.gentimeline1,name='gentimeline1'),
    path("absent",views.absent,name="absent"),
    path("localsms",views.localsms,name="localsms"),
    path("localsms1",views.localsms1,name="localsms1"),

]