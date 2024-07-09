from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Customs(AbstractUser):
    bank = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    ifsc_code = models.IntegerField(null=True,blank=True)
    pincode = models.IntegerField(null=True,blank=True)
    acnt_no = models.IntegerField(null=True,blank=True)
    amount = models.IntegerField(null=True,blank=True)
    phone_no = models.IntegerField(null=True,blank=True)
    address = models.CharField(max_length=50)
    adhar_no = models.IntegerField(null=True,blank=True)
    pancard_no = models.IntegerField(null=True,blank=True)
    image = models.FileField()
    dob = models.CharField(max_length=50)
    user_type = models.CharField(max_length=50)
    def __str__(self):
        return self.username
class Transaction(models.Model):
    user_id = models.IntegerField()
    details = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)
    user_amount = models.IntegerField()

