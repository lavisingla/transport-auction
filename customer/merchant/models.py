from django.db import models
from user_auth.models import user_info
from django.contrib.auth.models import User

class Company(models.Model):
    CompanyName = models.CharField(max_length=40)
    CompanyGST = models.CharField(max_length=50)
    Location = models.TextField(verbose_name="Company's base location")
    Owner = models.ForeignKey(user_info,on_delete=models.CASCADE) # foreign key with merchant
    PhoneNo = models.IntegerField(verbose_name="Company Phone No")
    Email = models.EmailField()
    

    def __str__(self):
        return self.CompanyName


class TruckInfo(models.Model):
    TruckName = models.CharField(max_length = 255)
    TruckId = models.CharField(max_length=10,verbose_name="Number Plate of Truck")
    PermitType = models.CharField(max_length = 25)
    Company = models.ForeignKey(Company,on_delete=models.CASCADE)
    PermitDate = models.DateField(verbose_name="Till when is the permit valid")

    def __str__(self):
        return "Truck Name: {} ----- Truck Id: {} ".format(self.TruckName,self.TruckId)



