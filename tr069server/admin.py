import imp
from django.shortcuts import redirect, render
from django.urls import path
from typing import List
from django import forms
from django.contrib import admin
from django.urls import URLPattern
from .models import Device,ProvisioningStatus
from .helperfunctions import validators as hvalidator
from .csvimporter.csvimport import DeviceCsvImport

# Creating a generic class for CSVimports to allow reuse of classes for 
    # any csv import that might be needed in the future other than devices
class CsvImportForm(forms.Form):
    csv_file  = forms.FileField()

# Creating a class Device admin which is extended from or inhereting from the admin.ModelAdmin class
class DeviceAdmin(admin.ModelAdmin):
    """Class to customize the admin view and functionality  """

    def get_urls(self) -> List[URLPattern]:
        """ add custom url path to admin url """

        urls = super().get_urls()
        new_urls = [path('csv_upload/',self.csv_file_upload)]
        return new_urls + urls
    
    def csv_file_upload(self, reqeust):
        """
            function to upload csv file
            CSV format
            CUSTOMERC_CODE;IPADDRESS ex. CUS001;4.6.4.5
        """        
        csv_form = CsvImportForm()        
        if reqeust.method == "POST":
           device_importer = DeviceCsvImport(reqeust.FILES["csv_file"])
           data_results = device_importer.import_data()
           data = {"form":csv_form,"results":data_results}
           
           if data_results is not None: 
                #Display error lines
               print("data results not true")
               return render(reqeust,"admin/tr069server/device/csv_upload.html", data)       
           
           print("import successful")    
           return redirect('/admin/tr069server/device')
            
        # if reqeust not POST
        data = {"form": csv_form}
        return render(reqeust,"admin/tr069server/device/csv_upload.html", data)

class ProvisioningStatusAdmin(admin.ModelAdmin):
    pass


admin.site.register(Device,DeviceAdmin)
admin.site.register(ProvisioningStatus,ProvisioningStatusAdmin), 
