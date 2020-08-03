from django import forms



from .models import *

from django.contrib.auth.models import User

class hw_info(forms.ModelForm):
   
    class Meta:
        model = worker_register
        

        fields = ('hw_fname','hw_sname','hw_addr','hw_adhar','hw_pincode','hw_phno','hw_district')
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password')

