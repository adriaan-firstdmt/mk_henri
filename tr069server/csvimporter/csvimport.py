from dataclasses import dataclass
from typing import Dict, List, Optional
from django import forms
from ..helperfunctions import validators as hvalidator
from ..models import Device,ProvisioningStatus
from django.db import IntegrityError

@dataclass
class FaultyLine:
    line:int
    fault_msg:str



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
    def validate_unique_ip(self,ipaddress:str) -> bool:
        devices = Device.objects.all()
        if devices.filter(ip=ipaddress).count() > 0:
            return False
        return True 
    def find_faulty_lines(self) -> List[FaultyLine]:
        faulty_lines:List[FaultyLine] = []
        for row_count, row in enumerate(self.csv_data):
            collums = row.split(self.delimiter)
            row_count =  row_count+1
            if not hvalidator.validate_ip(collums[1]):
                faulty_lines.append(FaultyLine(row_count,fault_msg=f"{collums[1]} invalid IP address"))
            if not hvalidator.validate_customercode(collums[0]):
                faulty_lines.append(FaultyLine(row_count,fault_msg=f"{collums[0]} invalid Customer Code"))
            if not self.validate_unique_ip(collums[1]):
                faulty_lines.append(FaultyLine(row_count,fault_msg=f"{collums[1]} not unique"))
        return faulty_lines

    def validate_csv_data(self) -> bool:
        """Validate IP address and CustomerCodes"""
        #Validation can also be added as custom validator in the model
        if len( self.find_faulty_lines() ) > 0:
            return False
        return True
    
    def import_data(self,strict=True) -> Optional[List[FaultyLine]]:
        """
            Import data from csv_file
            if strict true invalid data will cause no data to be imported 
        """
        is_vailidated = self.validate_csv_data()
       
        if strict and is_vailidated is not True:
            return self.find_faulty_lines()
        
        for row in self.csv_data:
            collums = row.split(self.delimiter)
            device = Device.objects.create(ip=collums[1],customer_code=collums[0])
            provisioningstatus = ProvisioningStatus(device=device,status=False)
            provisioningstatus.save()

        

    

