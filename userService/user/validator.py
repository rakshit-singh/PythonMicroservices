"""
The class is a validator class containing all the custom validators created for validation of DB models
"""
import re
from django.core.exceptions import ValidationError

def validatePhoneNo(number):
    regex = re.compile("[7-9][0-9]{9}")
    if not (regex.match(str(number))):
        raise ValidationError(message=('Invalid Phone Number'))