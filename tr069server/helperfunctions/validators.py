import ipaddress
from django.core.exceptions import ValidationError

def validate_ip(address):
    # using custom validator in order to allow for check in private,public ip, ranges, locals etc 
    try:
        ip = ipaddress.ip_address(address)
    except ValueError:
        return False
        # raise ValidationError(
            # '{ipaddr} is not an IP address'.format(ipaddr=address)
            # )
    return True

def validate_customercode(value,max_length=8):
    # check whether aplhanumeric
    if  not value.isalnum():
        return False
        # raise ValidationError(
        #    '{value} is not an alphanumeric string'.format(value=value)
        #    )
    # check max_length of string default max_length is 8
    if not len(value) <= max_length:
        return False
        # raise ValidationError(
        #    "{value} is larger than {max_length} characters".format(value=value,max_length=max_length)
        #    )
    return True