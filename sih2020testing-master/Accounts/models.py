from django.db import models
from django.contrib.auth.models import User

class worker_register(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,default=None)
    hw_fname = models.CharField(max_length=30,default=None)
    hw_sname = models.CharField(max_length=30,default=None)
    hw_adhar = models.CharField(max_length=12,default=None)
    hw_addr = models.CharField(max_length=200,default=None)
    hw_pincode = models.CharField(max_length=6,default=None)
    hw_district = models.CharField(max_length=20,default=None)
    hw_phno = models.CharField(max_length=13,default=None)
    
    def __str__(self):
        return self.hw_fname

    