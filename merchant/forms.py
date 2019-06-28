from django import forms
from merchant.models import Company,TruckInfo
from customer.models import order_bets

class CompanyForm(forms.ModelForm):
    class Meta():
        model=Company
        fields=('CompanyName','CompanyGST','Location','Owner','PhoneNo','Email')

class TruckForm(forms.ModelForm):
    class Meta():
        model  =TruckInfo
        fields =('TruckName','TruckId','PermitType','Company','PermitDate') 

class order_betsForm(forms.ModelForm):
    class Meta():
        model = order_bets
        fields = ('order_id','merchant_id','bet_price','extra_info','date_of_bet','pickup_days')
        #widgets = {'merchant_id':forms.HiddenInput()}

    
    def __init__(self, *args, **kwargs):
       
        self.order_id = kwargs.pop('order_id',None)
        self.merchant_id = kwargs.pop('merchant_id',None)
        super(order_betsForm, self).__init__(*args, **kwargs)

    def save(self,*args,**kwargs):
        self.instance.order_id = self.order_id
        self.instance.merchant_id = self.merchant_id
        obj = super(order_betsForm,self).save(*args,**kwargs)
        return obj