from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField

class beneficiary_info(forms.ModelForm):
    u_DOB = forms.DateField(widget=AdminDateWidget)

    class Meta:
        model = beneficiary_register
        fields = ('u_fname','u_sname','u_mother','u_father','u_adhar','u_addr','u_DOB','u_type','u_pincode','u_states','u_phno','u_phone','u_district','u_status','u_verified','u_ration','u_edu')        
        widgets = {'u_phno': forms.HiddenInput()} 
       
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password')
        
        
class usr(forms.ModelForm):
    class Meta:
        model = userbmi
        fields = '__all__'
        widgets = {'currentbmi': forms.HiddenInput(),'bmworker': forms.HiddenInput()} 