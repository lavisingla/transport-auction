from django.db import models
from user_auth.models import user_info
from django.contrib.auth.models import User
from customer.models import items

class MerchantManager(models.Manager):
    def get_company_details(self,merchant):
        return self.filter(Owner=merchant)

    def get_truck_details(self,company):
        return self.filter(Company=company)

    def get_permitted_states(self,company_id):
        return self.filter(company_id=company_id)

    def get_services(self,company_id):
        return self.filter(company_id=company_id)


class permitted_states(models.Model):
    company_id=models.PositiveIntegerField()
    state=models.CharField(max_length=30)
    objects = MerchantManager()

class services_provided(models.Model):
    company_id=models.PositiveIntegerField()
    services = models.ForeignKey(items,on_delete=models.CASCADE)
    objects = MerchantManager()

class Company(models.Model):
    CompanyName = models.CharField(max_length=40)
    CompanyGST = models.CharField(max_length=50)
    Location = models.TextField(verbose_name="Company's base location")
    Owner = models.ForeignKey(user_info,on_delete=models.CASCADE) # foreign key with merchant
    PhoneNo = models.IntegerField(verbose_name="Company Phone No")
    Email = models.EmailField()
    objects = MerchantManager()




    def __str__(self):
        return self.CompanyName


class TruckInfo(models.Model):
    TruckName = models.CharField(max_length = 255)
    TruckId = models.CharField(max_length=10,verbose_name="Number Plate of Truck")
    PermitType = models.CharField(max_length = 25)
    Company = models.ForeignKey(Company,on_delete=models.CASCADE)
    PermitDate = models.DateField(verbose_name="Till when is the permit valid")
    Truck_capacity=models.DecimalField(max_digits=20,decimal_places=2,default=1.00)
    Truck_length=models.DecimalField(max_digits=20,decimal_places=2,default=1.00)
    Truck_width=models.DecimalField(max_digits=20,decimal_places=2,default=1.00)
    objects = MerchantManager()
    def __str__(self):
        return "Truck Name: {} ----- Truck Id: {} ".format(self.TruckName,self.TruckId)
