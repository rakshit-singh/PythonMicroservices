from pickle import TRUE
from django.db import models
from django.core import validators

from .validator import validatePhoneNo

class User(models.Model):

    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20)
    email_id = models.EmailField(max_length=220, blank=False, unique=True)
    phone_number = models.CharField(max_length=10, blank=False, validators=[validatePhoneNo], unique=TRUE)

    def __str__(self):
        return '{} : {} : {} : {}'.format(self.first_name, self.last_name, self.email_id, self.phone_number)



    