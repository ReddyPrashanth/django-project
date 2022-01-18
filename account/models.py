from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
import re

# Create your models here.
def valid_zipcode(value):
    pattern = re.compile(r"[0-9]{5}")
    if pattern.match(value):
        return value
    else:
        raise ValidationError("Zipcode must contain five digits only.")

def valid_phone_number(value):
    pattern = re.compile(r"[0-9]{10}")
    if pattern.match(value):
        return value
    else:
        raise ValidationError("Phone number is not valid. Should not contain any characters.")
 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    job = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)
    zipcode = models.CharField(max_length=5, validators=[valid_zipcode])
    
    def __str__(self):
        return self.job