from typing import Dict
from django import forms
from ..helperfunctions import validators as hvalidator
from ..models import Device,ProvisioningStatus
from django.db import IntegrityError

class CsvImport:
    csv_file = None
    csv_data = None
    delimiter = ";"
    def __init__(self,csv_file,delimiter=";") -> None:
        self.csv_file = csv_file
        self.csv_data = self.csv_file.read().decode("utf-8").split()
        self.delimiter = delimiter

# TODO add Line fault dataclass or similar class to improve future  handeling of line faults

class DeviceCsvImport(CsvImport):
    def validate_unique_ip(self,ipaddress):
        devices = Device.objects.all()
        if devices.filter(ip=ipaddress).count() > 0:
            return False
        return True 

    def validate_csv_data(self):
        # TODO refactor to 2 methods one returning Bool for is valid 
        # and 1 for returning invalid data
        faulty_line = []
        """Validate IP address and CustomerCodes"""
        #Validation van also be added as custom validator in the model

        for row_count, row in enumerate(self.csv_data):
            collums = row.split(self.delimiter)
            row_count =  row_count+1
            if not hvalidator.validate_ip(collums[1]):
                faulty_line.append( {
                        'line':row_count,
                        'value':collums[1],
                        'msg':'{} is not a valid Ipaddress'.format(collums[1]) })
            if not hvalidator.validate_customercode(collums[0]):
                faulty_line.append({
                    'line':row_count,
                    'value':collums[0],
                    'msg':'{} is not a valid Customer Code'.format(collums[0])
                })
            if not self.validate_unique_ip(collums[1]):
                faulty_line.append({
                    "line":row_count+1,
                    "value": collums[1],
                    "msg" : "{} already exist".format(collums[1])
                })
        if len(faulty_line) > 0:
            return faulty_line
        
        return True
    
    def import_data(self,strict=True) -> Dict:
        """
            Import data from csv_file
            if strict true invalid data will not be cause no data to be imported 
        """
        data_results = self.validate_csv_data()
       
        if strict and data_results is not True:
            return data_results
        
        for row_count,row in enumerate(self.csv_data):
            collums = row.split(self.delimiter)
            device = Device.objects.create(ip=collums[1],customer_code=collums[0])
            # print(device)
            provisioningstatus = ProvisioningStatus(device=device,status=False)
            provisioningstatus.save()

        return data_results
        

    

