from django import forms
from merchant.models import Company,TruckInfo

class CompanyForm(forms.ModelForm):
    class Meta():
        model=Company
        fields=('CompanyName','CompanyGST','Location','Owner','PhoneNo','Email')

class TruckForm(forms.ModelForm):
    class Meta():
        model  =TruckInfo
        fields =('TruckName','TruckId','PermitType','Company','PermitDate') 
