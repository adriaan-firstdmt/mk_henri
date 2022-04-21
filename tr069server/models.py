from operator import mod
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import ipaddress
from .helperfunctions import validators as hvalidator


def validate_ip(address):
    # using custom validator in order to allow for check in private,public ip, ranges, locals, IPv6 etc 
    try:
        ip = ipaddress.ip_address(address)
    except ValueError:
        raise ValidationError(
            _('%(value)s is not an IP address'),params={'value':address}
            )

# Create your models here.
class Device(models.Model):
    # ip = models.GenericIPAddressField is the more common declartion in django of an field representing IP Address
        # and it comes with built in validation and some usefull helper functions 
    ip = models.CharField(max_length=15,unique=True,validators=[validate_ip])
    customer_code = models.CharField(max_length=255,default="",unique=True)

    def __str__(self):
        return f"{self.customer_code}  {self.ip}"
   
class ProvisioningStatus(models.Model):
    device = models.OneToOneField(Device, to_field='ip',db_column='ip',on_delete=models.CASCADE,primary_key=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"CUST:{self.device.customer_code} IP:{self.device.ip} STATUS:{self.status}"

